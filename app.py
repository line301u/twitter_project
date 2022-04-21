from bottle import run, get, static_file

###############################
import welcome_page_get   # GET
import home_get           # GET
import logout_get         # GET
import user_profile_get   # GET
import admin_panel_get    # GET
import send_email_get     # GET

import signup_post       # POST
import login_post        # POST
import tweet_post        # POST
import follow_post       # POST
import like_post         # POST

import tweet_delete    # DELETE
import follow_delete   # DELETE
import like_delete     # DELETE

import tweet_update       # PUT

###############################
@get("/app.css")
def _():
    return static_file("app.css", root="./css")

###############################
@get("/app.css.map")
def _():
    return static_file("app.css.map", root="./css")

#####################################
@get("/app.js")
def _():
    return static_file("app.js", root="./script")

#####################################
@get("/validator.js")
def _():
    return static_file("validator.js", root="./script")

#####################################
@get("/user/app.js")
def _():
    return static_file("app.js", root="./script")

#####################################
@get("/user/validator.js")
def _():
    return static_file("validator.js", root="./script")

##############################
@get("/images/tweet_images/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/tweet_images")

##############################
@get("/images/user_profile_pictures/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/user_profile_pictures")

##############################
@get("/images/welcome_page/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/welcome_page")

###############################
run(host="127.0.0.1", port="3333", debug=True, reloader=True)

