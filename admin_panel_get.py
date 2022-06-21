from bottle import get, view
import sqlite3
from get_dictonary import dict_factory

@get("/admin_panel")
@view("admin_panel")
def _():
    try:
        # CONNECT TO DB
        db_connection = sqlite3.connect("./database/database.sql")
        db_connection.row_factory = dict_factory

        tweets = db_connection.execute("""
        SELECT tweets.*, strftime('%d-%m-%Y', tweets.tweet_created_at, 'unixepoch') as tweet_created_at_formatted, users.user_id, users.user_name, users.user_profile_picture_path, users.user_first_name, users.user_last_name
        FROM tweets
        LEFT OUTER JOIN users
        ON tweets.fk_user_id = users.user_id
        ORDER BY tweets.tweet_created_at DESC
        """).fetchall()

        # CLOSE DB
        db_connection.close()

        return dict(tweets=tweets)
        
    except Exception as ex:
        print(ex)