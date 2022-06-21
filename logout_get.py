from bottle import get, request, redirect
import g
import sqlite3
import jwt

@get("/logout")
def _():
    try:
        # GET SESSION ID FROM COOKIE
        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
        user_session_id = encoded_user_information["user_session_id"]

        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            # REMOVE SESSION_ID FROM SESSIONS
            db_connection.execute("""
            DELETE FROM sessions
            WHERE user_session_id = ?
            """, (user_session_id, ))

            # SUCESS
            db_connection.commit()

            # CLOSE DB
            db_connection.close()

        return redirect("/")

    except Exception as ex:
        raise
        print(ex)
        return "something went wrong"

