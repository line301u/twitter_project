export {postTweet, displayTweet}
import covertEpochToDateTime from "./helpers.js"
import {openViewMoreOptions, closeViewMoreOptions} from "./toggleClasses.js"
import {openEditTweet} from "./editTweet.js"
import {deleteTweet} from "./deleteTweet.js"
import {backendErrorsValidation} from "./validator.js"

////////////////////////////////
// CREATE TWEET
export default async function postTweet(event){
    const form = event.target;

    const connection = await fetch("/tweet", {
        method: "POST",
        body: new FormData(form)
    });

    if (!connection.ok){
        console.log("connection failed")
        alert("could not tweet")
    };

    const response = await connection.json();

    if (response.error === "not an image file"){
        const ErrorInputElement = form.querySelector(".file_upload_icon");
        const errorMessage = "Filetypes allowed: jpg, jpeg, png";
        backendErrorsValidation(ErrorInputElement, errorMessage, "file");
        return;
    }

    // SUCESS
    const tweet = response;

    displayTweet(tweet);

    form.querySelector("#image_upload").value = "";
    form.querySelector(".tweet_text").value = "";
    form.querySelector(".filename").textContent = "";
    form.querySelector(".checkmark").classList.add("hidden");
}

////////////////////////////////
// DISPLAY POSTED TWEET
async function displayTweet(tweet){
    const container = document.querySelector(".tweets_wrapper");
    const template = document.querySelector('.tweet_template');

    if ('content' in document.createElement('template')) {
        // CREATE CLONE OF TWEET TEMPLATE
        const clone = template.content.cloneNode(true);

        clone.querySelector("form").classList.add(`tweet-${tweet.tweet_id}`);
        clone.querySelector(".tweet_id").value = tweet.tweet_id;
        clone.querySelector(".user_id").value = tweet.fk_user_id;

        if (tweet.user_profile_picture_path && tweet.user_profile_picture_path !== "0"){
            clone.querySelector(".user_profile_picture").src = `../images/user_profile_pictures/${tweet.user_profile_picture_path}`;
        } else {
            clone.querySelector(".user_profile_picture").src = "../images/user_profile_pictures/fallback_profile_picture.png";
        }

        clone.querySelector(".user_first_name").textContent = tweet.user_first_name;
        clone.querySelector(".user_info a").href = `/user/${tweet.fk_user_id}`;

        if (tweet.user_last_name) {
            clone.querySelector(".user_last_name").textContent = "\xa0" + tweet.user_last_name;
        }

        // CONVERT EPOCH TO DATETIME
        let timestamp = tweet.tweet_created_at;
        let converted_epoch = covertEpochToDateTime(timestamp);

        clone.querySelector(".tweet_created_at").textContent = ` · ${converted_epoch}`;
        clone.querySelector(".user_name").textContent = `@${tweet.user_name}`;
        clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
        clone.querySelector(".tweet_image_path").value = tweet.tweet_image_path;

        if (tweet.tweet_image_path && tweet.tweet_image_path !== "0"){
            clone.querySelector(".tweet_image").src = `../images/tweet_images/${tweet.tweet_image_path}`;
        } else {
            clone.querySelector(".tweet_image").classList.add("hidden")
        }

        container.insertBefore(clone, container.children[0]);

        const elementToAddEvents = document.querySelector(`.tweet-${tweet.tweet_id}`)
        elementToAddEvents.querySelector(".underlay")?.addEventListener('click', (event) => closeViewMoreOptions(event));
        elementToAddEvents.querySelector(".view-more")?.addEventListener('click', (event) => openViewMoreOptions(event));
        elementToAddEvents.querySelector(".edit_tweet")?.addEventListener('click', (event) => openEditTweet(event));
        elementToAddEvents.querySelector(".delete_tweet")?.addEventListener('click', (event) => deleteTweet(event));
    }
}
