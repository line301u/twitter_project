from bottle import post, response, request, get
import re
import g
import jwt
import sqlite3

@post("/like-tweet/<tweet_id>")
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
        
        if str(encoded_user_information["user_id"]) == request.forms.get("user_id"):
            return "user cannot like their own tweets"

        # SUCESS
        user_id = encoded_user_information["user_id"]
        tweet_id = tweet_id

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        # INSERT LIKE TO DB
        if db_connection:
            db_connection.execute("""
            INSERT INTO likes(fk_user_id, fk_tweet_id)
            VALUES(?, ?)
            """, (user_id, tweet_id))

        db_connection.commit()

        # CLOSE DB
        db_connection.close()

        return "like created"
    
    except Exception as ex:
        print(ex)

