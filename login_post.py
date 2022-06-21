from bottle import post, get, response, request, redirect
import g
import sqlite3
import re
import uuid
from get_dictonary import dict_factory
import jwt

@post("/login")
def _():
    try:
        # VALIDATE INPUTS
        if not request.forms.get("user_email"):
            response.status = 400
            return "User email missing"

        if len(request.forms.get("user_email")) > g.MAX_LENGHT_USER_EMAIL: 
            response.status = 400
            return "User email too long"

        if not re.match(g.REGEX_EMAIL, request.forms.get("user_email")):
            response.status = 400
            return "Not a valid email"
        
        if not request.forms.get("user_password"):
            response.status = 400
            return "User password is missing"

        if len(request.forms.get("user_password")) < g.MIN_LENGHT_USER_PASSWORD:
            response.status = 400
            return "User password is too short"

        if len(request.forms.get("user_password")) > g.MAX_LENGHT_USER_PASSWORD:
            response.status = 400
            return "User password is too long"

        # SUCESS
        user_email = request.forms.get("user_email").lower()
        user_password = request.forms.get("user_password")
        
        user = {
            "user_email" : user_email,
            "user_password" : user_password
        }

    except Exception as ex:
        raise
        print(ex)

    try:
        # CONNECT TO DB
        db_connection = sqlite3.connect("./database/database.sql")
        if db_connection:
            db_connection.row_factory = dict_factory

            # GET USER BY EMAIL
            user_db = db_connection.execute("""
            SELECT * 
            FROM users
            WHERE user_email = (:user_email)
            """, user).fetchone()

            if not user_db:
                response.status = 400
                print("email is not in db")
                return "email error"

            if user_db and not user_password == user_db["user_password"]:
                response.status = 400
                print("Wrong password")
                return "password error"

            # CHECK IF USER IS IN DB
            if user_db and user_password == user_db["user_password"]:
                user_session_information = {
                    "user_session_id" : str(uuid.uuid4())
                }

                # ADD USER SESSIONS ID TO DB
                db_connection.execute("""
                INSERT INTO sessions
                VALUES(:user_session_id)
                """, user_session_information)

                db_connection.commit()

                # CLOSE DB
                db_connection.close()

                user_information = {
                    "user_name" : user_db["user_name"],
                    "user_session_id" : user_session_information["user_session_id"],
                    "user_id" : user_db["user_id"]
                }

                encoded_jwt = jwt.encode(user_information, g.COOKIE_SECRET, algorithm="HS256")
                response.set_cookie("user_information", encoded_jwt, secret=g.COOKIE_SECRET)

                redirect("/home")

        return redirect("/")

    except Exception as ex:
        raise
        print(ex)
