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
        user_information = request.get_cookie("user_information")
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
    
    except Exception as ex:
        print(ex)
    
    finally:
        if db_connection:
            db_connection.close()
    
    try:
        db_connection = sqlite3.connect("./database/database.sql")
        db_connection.row_factory = dict_factory

        tweets = db_connection.execute("""
        SELECT tweets.*, users.user_name, users.user_profile_picture_path, users.user_first_name, users.user_last_name
        FROM tweets
        LEFT OUTER JOIN users
        ON tweets.fk_user_id = users.user_id
        ORDER BY tweets.tweet_created_at DESC
        """).fetchall()

        users = db_connection.execute("""
        SELECT users.user_id, users.user_name, users.user_first_name, users.user_last_name, followers.fk_follow_initiator as followed_by_user
        FROM users
        LEFT OUTER JOIN followers 
        ON followers.fk_follow_reciever = users.user_id and followers.fk_follow_initiator = ?
        WHERE users.user_id != ?
        LIMIT 4;
        """, (user_id, user_id)).fetchall()

        print(30*"#")
        print(users)

        return dict(tweets=tweets, users=users)
        
    except Exception as ex:
        print(ex)

    finally:
        if db_connection:
            db_connection.close()
