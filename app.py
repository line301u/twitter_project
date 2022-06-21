from bottle import run, get, static_file, default_app

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


##############################
# GET STYLESHEETS
##############################
@get("/app.css")
def _():
    return static_file("app.css", root="./styles/css")

##############################
@get("/app.css.map")
def _():
    return static_file("app.css.map", root="./styles/css")


##############################
# GET SCRIPTS
##############################
@get("/app.js")
def _():
    return static_file("app.js", root="./script")

##############################
@get("/createUser.js")
def _():
    return static_file("createUser.js", root="./script")

##############################
@get("/loginUser.js")
def _():
    return static_file("loginUser.js", root="./script")

##############################
@get("/helpers.js")
def _():
    return static_file("helpers.js", root="./script")

##############################
@get("/eventHandlers.js")
def _():
    return static_file("eventHandlers.js", root="./script")

##############################
@get("/editTweet.js")
def _():
    return static_file("editTweet.js", root="./script")

##############################
@get("/deleteTweet.js")
def _():
    return static_file("deleteTweet.js", root="./script")

##############################
@get("/postTweet.js")
def _():
    return static_file("postTweet.js", root="./script")

##############################
@get("/validator.js")
def _():
    return static_file("validator.js", root="./script")

##############################
@get("/toggleClasses.js")
def _():
    return static_file("toggleClasses.js", root="./script")

##############################
@get("/tweetLikes.js")
def _():
    return static_file("tweetLikes.js", root="./script")

##############################
@get("/userFollow.js")
def _():
    return static_file("userFollow.js", root="./script")

##############################
@get("/user/app.js")
def _():
    return static_file("app.js", root="./script")

##############################
@get("/user/createUser.js")
def _():
    return static_file("createUser.js", root="./script")

##############################
@get("/user/toggleClasses.js")
def _():
    return static_file("toggleClasses.js", root="./script")

##############################
@get("/user/userFollow.js")
def _():
    return static_file("userFollow.js", root="./script")

##############################
@get("/user/validator.js")
def _():
    return static_file("validator.js", root="./script")

##############################
@get("/user/loginUser.js")
def _():
    return static_file("loginUser.js", root="./script")

##############################
@get("/user/eventHandlers.js")
def _():
    return static_file("eventHandlers.js", root="./script")

##############################
@get("/user/postTweet.js")
def _():
    return static_file("postTweet.js", root="./script")

##############################
@get("/user/editTweet.js")
def _():
    return static_file("editTweet.js", root="./script")

##############################
@get("/user/tweetLikes.js")
def _():
    return static_file("tweetLikes.js", root="./script")

##############################
@get("/user/deleteTweet.js")
def _():
    return static_file("deleteTweet.js", root="./script")

##############################
@get("/user/helpers.js")
def _():
    return static_file("helpers.js", root="./script")


##############################
@get("/images/tweet_images/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/tweet_images")


##############################
# GET IMAGES
##############################
@get("/images/user_profile_pictures/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/user_profile_pictures")

##############################
@get("/images/welcome_page/<image_name>")
def _(image_name):
    return static_file(image_name, root="./images/welcome_page")


##############################
try:
    import production
    application = default_app()
    
except Exception as ex:
    print("Server running on development")
    run(host="127.0.0.1", port="3333", debug=True, reloader=True)
