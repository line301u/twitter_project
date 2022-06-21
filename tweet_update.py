from bottle import get, put, request, redirect, response
import g
import time
import imghdr
import os
import uuid
import sqlite3

@put("/update-tweet/<tweet_id>")
def _(tweet_id):
    try:
        # VALIDATION
        if not request.forms.get("tweet_text"):
            response.status = 400
            return "tweet_text is missing"
        if len(request.forms.get("tweet_text")) > g.MAX_LENGHT_TWEET_TEXT:
            response.status = 400
            return f"tweet_text is too long, the max amount of characters is {g.MAX_LENGHT_TWEET_TEXT}"
        if not tweet_id:
            response.status = 204
            return "tweet_id missing"

        # CHECK IF TWEET ID IS IN DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            tweet_id_from_db = db_connection.execute("SELECT tweet_id FROM tweets WHERE tweet_id = ?",(tweet_id,)).fetchone()
            print(tweet_id_from_db)
            if tweet_id_from_db != None:
                tweet_id_from_db = str(tweet_id_from_db[0])

            if tweet_id != tweet_id_from_db or tweet_id_from_db == None:
                response.status = 400
                return "tweet_id not is not in database"

        # CLOSE DB
            db_connection.close()

        # VALIDATE IMAGE
        tweet_image = request.files.get("tweet_image")

        if tweet_image:
            file_name, file_extension = os.path.splitext(tweet_image.filename)

            # VALIDATE EXTENSION
            if file_extension not in (".png", ".jpeg", ".jpg", ".JPG", ".heic", ".HEIC"):
                response.status = 400
                return "image not allowed"

            # OVERWRITE JPG TO JPEG SO IMGHDR WILL PASS VALIDATION
            if file_extension == ".jpg": file_extension = ".jpeg"
            if file_extension == ".JPG": file_extension = ".jpeg"

            # CREATE IMAGE NAME
            image_id = str(uuid.uuid4())
            tweet_image_name = f"{image_id}{file_extension}"

            # VALIDATE IMAGE NAME
            if len(tweet_image_name) > g.MAX_LENGHT_IMAGE_PATH:
                return "file name is too long"

            print(f"./images/tweet_images/{tweet_image_name}")
            # SAVE IMAGE
            tweet_image.save(f"./images/tweet_images/{tweet_image_name}")

            # VALIDATE IMAGE FILE 
            imghdr_extension = imghdr.what(f"./images/tweet_images/{tweet_image_name}")

            if file_extension != f".{imghdr_extension}":
                os.remove(f"./images/tweet_images/{tweet_image_name}")
                print("not an image file")
                return {"error" : "not an image file"}

        # SUCESS
        tweet_text = request.forms.get("tweet_text")
        tweet_updated_at = int(time.time())
        tweet_image_path = request.forms.get("tweet_image_path")

        if tweet_image and tweet_image_path != tweet_image_name : tweet_image_path = tweet_image_name

        updated_tweet = {
            "tweet_id" : tweet_id,
            "tweet_text" : tweet_text,
            "tweet_image_path" : tweet_image_path,
            "tweet_updated_at" : tweet_updated_at
        }

    except Exception as ex:
        print(ex)

    try:
        # CONNECT TO DATABASE
        db_connection = sqlite3.connect("./database/database.sql")

        if db_connection:
            counter = db_connection.execute("""
            UPDATE tweets
            SET tweet_text = :tweet_text, tweet_image_path = :tweet_image_path, tweet_updated_at = :tweet_updated_at
            WHERE tweet_id = :tweet_id
            """, updated_tweet).rowcount

            # SUCSESS
            db_connection.commit()

            # CLOSE DB
            db_connection.close()

            return updated_tweet
    
    except Exception as ex:
        print(ex)
