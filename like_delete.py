from bottle import delete, get, response, request
import g
import jwt
import re
import sqlite3


@delete("/unlike-tweet/<tweet_id>")
def _(tweet_id):
    try:
        # VALIDATION
        if not tweet_id:
            response.status = 204
            return "tweet_id is missing"

        if not re.match(g.REGEX_ID, tweet_id):
            response.status = 400
            return "tweet_id is not valid"
        
        # GET USER_ID FROM COOKIE
        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")

        if not encoded_user_information["user_id"]:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_ID, str(encoded_user_information["user_id"])):
            response.status = 400
            return "user_id is not valid"
        
        if str(encoded_user_information["user_id"]) == encoded_user_information["user_id"]:
            return "user cannot like tweets by itself"

        # SUCESS
        user_id = encoded_user_information["user_id"]
        tweet_id = tweet_id

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            # CHECK IF LIKE EXISTS
            tweet_is_liked_by_user = db_connection.execute("""
            SELECT *
            FROM likes
            WHERE fk_user_id = ? and fk_tweet_id = ?
            """, (user_id, tweet_id)).fetchone()
            print(tweet_is_liked_by_user)

            if not tweet_is_liked_by_user:
                return "like doesnt exist"
            
            # DELETE LIKE
            db_connection.execute("""
            DELETE FROM likes
            WHERE fk_user_id = ? and fk_tweet_id = ?
            """, (user_id, tweet_id)).rowcount

            db_connection.commit()

            # CLOSE DB
            db_connection.close()

            return "like deleted"

    except Exception as ex:
        print(ex)