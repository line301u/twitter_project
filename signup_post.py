from bottle import post, response, redirect, request, get
import g
import re
import imghdr
import os
import uuid
import sqlite3
import time
from send_email_get import send_email

@post("/signup")
def _():
    try:
        # INPUT VALIDATION
        if not request.forms.get("user_name"):
            response.status = 400
            return "username missing"

        if len(request.forms.get("user_name")) > g.MAX_LENGHT_USER_NAME: 
            response.status = 400
            return "username too long"

        if not request.forms.get("user_first_name"):
            response.status = 400
            return "first name missing"

        if len(request.forms.get("user_first_name")) > g.MAX_LENGHT_USER_FIRST_NAME: 
            response.status = 400
            return "username too long"
        
        if request.forms.get("user_last_name"):
            if len(request.forms.get("user_last_name")) > g.MAX_LENGHT_USER_LAST_NAME: 
                response.status = 400
                return "last name too long"

        if not request.forms.get("user_email"):
            response.status = 400
            return "email missing"

        if len(request.forms.get("user_email")) > g.MAX_LENGHT_USER_EMAIL: 
            response.status = 400
            return "user email too long"

        if not re.match(g.REGEX_EMAIL, request.forms.get("user_email")):
            response.status = 400
            return "user email not valid"

        if not request.forms.get("user_password"):
            response.status = 400
            return "password missing" 

        if len(request.forms.get("user_password")) < g.MIN_LENGHT_USER_PASSWORD: 
            response.status = 400
            return "password too short"

        if len(request.forms.get("user_password")) > g.MAX_LENGHT_USER_PASSWORD: 
            response.status = 400
            return "password too long"

        # VALIDATE PROFILE IMAGE
        user_profile_picture = request.files.get("user_profile_picture")

        if user_profile_picture:
            file_name, file_extension = os.path.splitext(user_profile_picture.filename)

            # VALIDATE EXTENSION
            if file_extension not in (".png", ".jpeg", ".jpg"):
                return "image not allowed"
            
            # OVERWRITE JPG TO JPEG SO IMGHDR WILL PASS VALIDATION
            if file_extension == ".jpg": file_extension = ".jpeg"
            
            # CREATE IMAGE NAME
            image_id = str(uuid.uuid4())
            image_name = f"{image_id}{file_extension}"

            # VALIDATE IMAGE NAME
            if len(image_name) > g.MAX_LENGHT_IMAGE_PATH:
                response.status = 400
                return "file name is too long"

            # SAVE IMAGE
            user_profile_picture.save(f"./images/user_profile_pictures/{image_name}")

            # VALIDATE IMAGE FILE 
            imghdr_extension = imghdr.what(f"./images/user_profile_pictures/{image_name}")

            if file_extension != f".{imghdr_extension}":
                print("not an image file")
                os.remove(f"./images/user_profile_pictures/{image_name}")
                return "Not an image file"

        # SUCESS
        user_name = request.forms.get("user_name")
        user_first_name = request.forms.get("user_first_name")
        user_last_name = request.forms.get("user_last_name")
        user_email = request.forms.get("user_email").lower()
        user_password = request.forms.get("user_password")
        user_profile_picture_path = False
        user_created_at = int(time.time())

        if user_profile_picture:
            user_profile_picture_path = image_name

        user = {
            "user_id" : None,
            "user_name" : user_name,
            "user_first_name" : user_first_name,
            "user_last_name" : user_last_name,
            "user_email" : user_email,
            "user_password" : user_password,
            "user_profile_picture_path" : user_profile_picture_path,
            "user_created_at" : user_created_at
        }

    except Exception as ex:
        # CHECK IF EMAIL AND USERNAME ALREADY IN SYSTEM IN SYSTEM
        if 'user_email' in str(ex):
            print("email already exists")
        
        if 'user_name' in str(ex):
            print("username already exists")
        
        return "something when wrong"

    try:
        db_connection = sqlite3.connect("./database/database.sql")
        if db_connection:
            db_connection.execute("INSERT INTO users VALUES(:user_id, :user_name, :user_first_name, :user_last_name, :user_email, :user_profile_picture_path, :user_created_at, :user_password)", user).rowcount
            # db_connection.commit()

            send_email(user)

    except Exception as ex: 
        print(ex)
        return "something went wrong"
        
    finally:
        db_connection.close()