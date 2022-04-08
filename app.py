from bottle import run, get, static_file

###############################
import welcome_page_get   # GET
import home_get           # GET
import logout_get         # GET

import signup_post       # POST
import login_post        # POST
import tweet_post        # POST
import follow_post       # POST

import tweet_delete    # DELETE
import follow_delete   # DELETE

import tweet_update       # PUT

###############################
@get("/app.css")
def _():
    return static_file("app.css", root="./css")

#####################################
@get("/app.js")
def _():
    return static_file("app.js", root="./script")

##############################
@get("/images/tweet_images/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/tweet_images")

##############################
@get("/images/user_profile_pictures/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/user_profile_pictures")

###############################
run(host="127.0.0.1", port="3333", debug=True, reloader=True)