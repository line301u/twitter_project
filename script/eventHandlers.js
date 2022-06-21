export {inputEventHandlers, submitEventHandlers, clickEventHandlers, onChangeEventHandlers}
import {toggleDisplaySignup, toggleDisplayLogin, openViewMoreOptions, closeViewMoreOptions, toggleLogout} from "./toggleClasses.js"
import {validate, clear_validate_error} from "./validator.js"
import createUser from "./createUser.js"
import loginUser from "./loginUser.js"
import postTweet from "./postTweet.js"
import deleteTweet from "./deleteTweet.js"
import {likeTweet, dislikeTweet} from "./tweetLikes.js"
import {createFollow, deleteFollow} from "./userFollow.js"
import {closeEditTweet, openEditTweet, updateTweet} from "./editTweet.js"
import {fileUploaded} from "./helpers.js"

////////////////////////////////
// CLICK EVENTS
export default function clickEventHandlers(){
    document.querySelector(".signup-close")?.addEventListener('click', () => toggleDisplaySignup());
    document.querySelector(".signup-button")?.addEventListener('click', () => toggleDisplaySignup());
    document.querySelector(".login-button")?.addEventListener('click', () => toggleDisplayLogin());
    document.querySelector(".login-close")?.addEventListener('click', () => toggleDisplayLogin());
    
    document.querySelector(".nav_user_info")?.addEventListener('click', () => toggleLogout());
    document.querySelector(".logout-wrapper .underlay")?.addEventListener('click', () => toggleLogout());

    document.querySelector(".tweets_wrapper .underlay")?.addEventListener('click', (event) => closeViewMoreOptions(event));

    document.querySelectorAll(".view-more")?.forEach(element => {
        element.addEventListener('click', (event) => openViewMoreOptions(event));
    });

    document.querySelectorAll(".edit_tweet_button")?.forEach(element => {
        element.addEventListener('click', (event) => openEditTweet(event));
    });
    
    document.querySelector(".cancel-edit")?.addEventListener('click', (event) => closeEditTweet(event));

    document.querySelector(".save_button")?.addEventListener('click', (event) => {
        event.preventDefault();
        validate(event, updateTweet);
    });

    document.querySelectorAll(".delete_tweet")?.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            validate(event, deleteTweet);
        });
    });

    document.querySelectorAll(".like-button")?.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            validate(event, likeTweet);
        });
    });

    document.querySelectorAll(".dislike-button")?.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            validate(event, dislikeTweet);
        });
    });

    document.querySelectorAll(".follow-button")?.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            validate(event, createFollow);
        });
    });

    document.querySelectorAll(".unfollow-button")?.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            validate(event, deleteFollow);
        });
    });
}

////////////////////////////////
// KEYUP EVENTS
function inputEventHandlers(inputs, amount){
        if (amount === "one"){
            inputs[0]?.addEventListener('keyup', (event) => clear_validate_error(event));
        }
        if (amount === "all"){
            inputs.forEach(input => {
                input?.addEventListener('keyup', (event) => clear_validate_error(event));
            });
        }
}

////////////////////////////////
// SUBMIT EVENTS
function submitEventHandlers(){
    document.querySelector(".signup-form")?.addEventListener('submit', (event) => {
        event.preventDefault();
        validate(event, createUser);
    });

    document.querySelector(".login-form")?.addEventListener('submit', (event) => {
        event.preventDefault();
        validate(event, loginUser);
    });
    
    document.querySelector(".post_tweet_form")?.addEventListener('submit', (event) => {
        event.preventDefault();
        validate(event, postTweet);
    });
}

////////////////////////////////
// CHANGE EVENTS
function onChangeEventHandlers(){
    document.querySelector(".post_tweet_form #image_upload")?.addEventListener('change', (event) => fileUploaded(event));
    document.querySelector(".edit_tweet #tweet_image")?.addEventListener('change', (event) => fileUploaded(event));
    document.querySelector(".signup-form-container #user_profile_picture")?.addEventListener('change', (event) => fileUploaded(event));
}
