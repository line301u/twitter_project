from bottle import get, delete, request, response
import g
import sqlite3

@delete("/delete-tweet/<tweet_id>")
def _(tweet_id):
    try:
        # VALIDATION
        if not tweet_id:
            response.status = 204
            return "no tweet_id"

        # CHECK IF ID IS IN DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            tweet_id_from_db = db_connection.execute("SELECT tweet_id FROM tweets WHERE tweet_id = ?",(tweet_id,)).fetchone()

            if tweet_id_from_db != None:
                tweet_id_from_db = str(tweet_id_from_db[0])

            if tweet_id != tweet_id_from_db or tweet_id_from_db == None:
                response.status = 400
                return "tweet_id not is not in database"

    except Exception as ex:
        print(ex)
        return "something went wrong"
    
    finally:
        db_connection.close()

    try:
        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")
        
        if db_connection:
            # DELETE TWEET BY ID
            db_connection.execute("""
            DELETE FROM tweets
            WHERE tweet_id = ?
            """, (tweet_id, ))

            db_connection.commit()

            # SUCESS
            return "tweet deleted"

    except Exception as ex:
        print(ex)
        return "something went wrong"

    finally:
        db_connection.close()
