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
        
        user_information = request.get_cookie("user_information")
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
        user_id = encoded_user_information["user_id"]

        if not user_id:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_USER_ID, user_id):
            response.status = 400
            return "user_id is not valid"

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DB
        db_connection = sqlite3.connect("./database/database.sql")
        db_connection.row_factory = dict_factory

        if db_connection:
            user = db_connection.execute("""
            SELECT users.*, followers.fk_follow_initiator as followed_by_user
            FROM users
            LEFT OUTER JOIN followers 
            ON followers.fk_follow_reciever = users.user_id and followers.fk_follow_initiator = ?
            WHERE user_id = ?
            """, (user_id, profile_user_id)).fetchone()

            tweets_by_user = db_connection.execute("""
            SELECT * 
            FROM tweets
            WHERE fk_user_id = ?
            """, (profile_user_id, )).fetchall()

            print(user)

            return dict(user=user, tweets=tweets_by_user)

    except Exception as ex:
        print(ex)
    
    finally:
        if db_connection:
            db_connection.close()