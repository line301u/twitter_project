from bottle import post, response, request, get
import re
import g
import jwt
import sqlite3

@post("/follow")
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
            return "user cannot follow itself"

        # SUCESS
        follow_initiator_user_id = encoded_user_information["user_id"]
        follow_reciever_user_id = request.forms.get("user_id")

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            db_connection.execute("""
            INSERT INTO followers(fk_follow_initiator, fk_follow_reciever)
            VALUES(?, ?)
            """, (follow_initiator_user_id, follow_reciever_user_id))

        db_connection.commit()

        return "follow created"
    
    except Exception as ex:
        print(ex)
    
    finally:
        if db_connection:
            db_connection.close()
