from bottle import get, view, request, response, redirect
import sqlite3
from get_dictonary import dict_factory
import json
import g
import jwt

@get("/home")
@view("home")
def _():
    try:
        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
        user_session_id = encoded_user_information["user_session_id"]
        user_id = encoded_user_information["user_id"]

        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            is_user_logged_in = db_connection.execute("SELECT user_session_id FROM sessions WHERE user_session_id = ?", (user_session_id, )).fetchone()

            # CHECK IF USER IS LOGGED IN
            if not is_user_logged_in:
                response.status = 204
                return redirect("/")
            
            # CLOSE DB
            db_connection.close()
    
    except Exception as ex:
        print(ex)
    
    try:
        db_connection = sqlite3.connect("./database/database.sql")
        db_connection.row_factory = dict_factory

        if db_connection:
            tweets = db_connection.execute("""
            SELECT tweets.*, strftime('%d-%m-%Y', tweets.tweet_created_at, 'unixepoch') as tweet_created_at_formatted, users.user_id, users.user_name, users.user_profile_picture_path, users.user_first_name, users.user_last_name, likes.fk_user_id as liked_by_user
            FROM tweets
            LEFT OUTER JOIN users
            ON tweets.fk_user_id = users.user_id
            LEFT OUTER JOIN likes
            ON likes.fk_tweet_id = tweets.tweet_id and likes.fk_user_id = ?
            ORDER BY tweets.tweet_created_at DESC
            """,(user_id, )).fetchall()

            user = db_connection.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
            """, (user_id, )).fetchone()

            users = db_connection.execute("""
            SELECT users.user_id, users.user_name, users.user_first_name, users.user_last_name, users.user_profile_picture_path, followers.fk_follow_initiator as followed_by_user
            FROM users
            LEFT OUTER JOIN followers 
            ON followers.fk_follow_reciever = users.user_id and followers.fk_follow_initiator = ?
            WHERE users.user_id != ?
            LIMIT 4;
            """, (user_id, user_id)).fetchall()

            db_connection.close()

            return dict(tweets=tweets, users=users, user=user)
        
    except Exception as ex:
        print(ex)
