from bottle import get, post, response, request
import g
import imghdr
import os
import time
import jwt
import sqlite3
import uuid
import json
from get_dictonary import dict_factory

@post("/tweet")
def _():
    try:
        # VALIDATE USER INPUTS
        if not request.forms.get("tweet_text"):
            response.status = 400
            return "Tweet text is missing"

        if len(request.forms.get("tweet_text")) > g.MAX_LENGHT_TWEET_TEXT:
            response.status = 400
            return "Tweet text is too long"

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
            image_name = f"{image_id}{file_extension}"

            # VALIDATE IMAGE NAME
            if len(image_name) > g.MAX_LENGHT_IMAGE_PATH:
                return "file name is too long"

            # SAVE IMAGE
            tweet_image.save(f"./images/tweet_images/{image_name}")

            # VALIDATE IMAGE FILE 
            imghdr_extension = imghdr.what(f"./images/tweet_images/{image_name}")

            if file_extension != f".{imghdr_extension}":
                print("not an image file")
                os.remove(f"./images/tweet_images/{image_name}")
                return {"error" : "not an image file"}

        # SUCESS
        tweet_text = request.forms.get("tweet_text")
        tweet_image_path = False
        if tweet_image : tweet_image_path = image_name
        tweet_created_at = int(time.time())

        user_information = request.get_cookie("user_information", secret=g.COOKIE_SECRET)
        encoded_user_information = jwt.decode(user_information, g.COOKIE_SECRET, algorithms="HS256")
        user_id = encoded_user_information["user_id"]

        tweet = {
            "tweet_id" : None,
            "tweet_text" : tweet_text,
            "tweet_image_path" : tweet_image_path,
            "tweet_created_at" : tweet_created_at,
            "tweet_updated_at" : None,
            "fk_user_id" : user_id
        }
        
    except Exception as ex:
        print(ex)

    try:
        db_connection = sqlite3.connect("./database/database.sql")
        
        db_connection.execute("""
        INSERT INTO tweets
        VALUES(:tweet_id, :tweet_text, :tweet_image_path, :tweet_created_at, :tweet_updated_at, :fk_user_id)
        """, tweet).rowcount

        db_connection.commit()

        tweet_id = db_connection.execute("SELECT last_insert_rowid()").fetchone()[0]

        db_connection.row_factory = dict_factory

        db_tweet = db_connection.execute("""
        SELECT tweets.*, users.user_name, users.user_profile_picture_path, users.user_first_name, users.user_last_name
        FROM tweets
        LEFT OUTER JOIN users 
        ON tweets.fk_user_id = users.user_id
        WHERE tweets.tweet_id = ?
        """,(tweet_id,)).fetchone()

        # CLOSE DB
        db_connection.close()

        db_tweet = json.dumps(db_tweet)

        return db_tweet

    except Exception as ex:
        print(ex)
