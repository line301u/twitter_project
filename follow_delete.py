from bottle import delete, get, response, request
import g
import jwt
import re
import sqlite3


@delete("/unfollow-user/<user_id>")
def _(user_id):
    try:
        # VALIDATION
        if not user_id:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_ID, user_id):
            response.status = 400
            return "user_id is not valid"
        
        # GET USER_ID FROM COOKIE
        user_information = request.get_cookie("user_information")
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")

        if not encoded_user_information["user_id"]:
            response.status = 204
            return "user_id is missing"

        if not re.match(g.REGEX_ID, str(encoded_user_information["user_id"])):
            response.status = 400
            return "user_id is not valid"
        
        if str(encoded_user_information["user_id"]) == user_id:
            return "user cannot unfollow itself"

        # SUCESS
        unfollow_initiator_user_id = encoded_user_information["user_id"]
        unfollow_reciever_user_id = user_id

    except Exception as ex:
        print(ex)

    try:
        db_connection = sqlite3.connect("./database/database.sql")

        # CHECK IF FOLLOW EXISTS
        user_is_followed_by_user = db_connection.execute("""
        SELECT *
        FROM followers
        WHERE fk_follow_initiator = ? and fk_follow_reciever = ?
        """, (unfollow_initiator_user_id, unfollow_reciever_user_id)).fetchone()
        print(user_is_followed_by_user)

        if not user_is_followed_by_user:
            return "follow doesnt exist"

        # DELETE FOLLOW
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