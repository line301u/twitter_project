from bottle import delete, get, response, request
import g
import jwt
import re
import sqlite3


@delete("/delete-follow")
def _():
    try:
        # VALIDATION
        if not request.forms.get("user_id"):
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_USER_ID, request.forms.get("user_id")):
            response.status = 400
            return "user_id is not valid"
        
        # GET USER_ID FROM COOKIE
        user_information = request.get_cookie("user_information")
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")

        if not encoded_user_information["user_id"]:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_USER_ID, str(encoded_user_information["user_id"])):
            response.status = 400
            return "user_id is not valid"
        
        if str(encoded_user_information["user_id"]) == request.forms.get("user_id"):
            return "user cannot unfollow itself"

        # SUCESS
        unfollow_initiator_user_id = encoded_user_information["user_id"]
        unfollow_reciever_user_id = request.forms.get("user_id")

    except Exception as ex:
        print(ex)

    try:
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            db_connection.execute("""
            DELETE FROM followers
            WHERE fk_follow_initiator = ? and fk_follow_reciever = ?
            """, (unfollow_initiator_user_id, unfollow_reciever_user_id)).rowcount

            db_connection.commit()
            
            return "follow deleted"

    except Exception as ex:
        print(ex)

    finally:
        if db_connection:
            db_connection.close()