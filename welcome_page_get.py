from bottle import get, view, redirect, response, request
import sqlite3
import g
import jwt

@get("/")
@view("index")
def _():
    try:
        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)

        if user_information:
            encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
            user_session_id = encoded_user_information["user_session_id"]

        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection and user_information:
            is_user_logged_in = db_connection.execute("SELECT user_session_id FROM sessions WHERE user_session_id = ?", (user_session_id, )).fetchone()

            # CHECK IF USER IS LOGGED IN
            if is_user_logged_in:
                return redirect("/home")
        
        return

    except Exception as ex:
        raise
        print(ex)
    
    finally:
        if db_connection:
            db_connection.close()
