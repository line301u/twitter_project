from bottle import get, view, response, request
import re
import g
import sqlite3
from get_dictonary import dict_factory
import jwt

@get("/user/<profile_user_id>")
@view("user_profile")
def _(profile_user_id):
    try:
        # VALIDATION
        if not profile_user_id:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_ID, profile_user_id):
            response.status = 400
            return "user_id is not valid"
        
        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
        user_id = encoded_user_information["user_id"]

        if not user_id:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_ID, user_id):
            response.status = 400
            return "user_id is not valid"

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DB
        db_connection = sqlite3.connect("./database/database.sql")
        db_connection.row_factory = dict_factory

        if db_connection:
            profile_user = db_connection.execute("""
            SELECT users.*, followers.fk_follow_initiator as followed_by_user, strftime('%d-%m-%Y', users.user_created_at, 'unixepoch') as user_created_at_formatted
            FROM users
            LEFT OUTER JOIN followers 
            ON followers.fk_follow_reciever = users.user_id and followers.fk_follow_initiator = ?
            WHERE user_id = ?
            """, (user_id, profile_user_id)).fetchone()

            tweets_by_user = db_connection.execute("""
            SELECT tweets.*, likes.fk_user_id as liked_by_user, strftime('%d-%m-%Y', tweets.tweet_created_at, 'unixepoch') as tweet_created_at_formatted
            FROM tweets
            LEFT OUTER JOIN likes
            ON likes.fk_tweet_id = tweets.tweet_id and likes.fk_user_id = ?
            WHERE tweets.fk_user_id = ?
            ORDER BY tweets.tweet_created_at DESC
            """,(user_id, profile_user_id)).fetchall()

            logged_in_user = db_connection.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
            """, (user_id, )).fetchone()

            user_recomendations = db_connection.execute("""
            SELECT users.user_id, users.user_name, users.user_first_name, users.user_last_name, users.user_profile_picture_path, followers.fk_follow_initiator as followed_by_user
            FROM users
            LEFT OUTER JOIN followers 
            ON followers.fk_follow_reciever = users.user_id and followers.fk_follow_initiator = ?
            WHERE users.user_id != ? and users.user_id != ?
            LIMIT 4;
            """, (user_id, user_id, profile_user_id)).fetchall()

            # CLOSE DB
            db_connection.close()

            return dict(profile_user=profile_user, tweets=tweets_by_user, user=logged_in_user, user_recomendations=user_recomendations)

    except Exception as ex:
        print(ex)
    