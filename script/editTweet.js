export {closeEditTweet, openEditTweet, updateTweet}
import {backendErrorsValidation} from "./validator.js"


////////////////////////////////
// OPEN EDIT TWEET VIEW
function openEditTweet(event){
    let targetTweet = event.target.form;
    const edit_tweet_form = document.querySelector(".edit_tweet_container")
    edit_tweet_form.classList.remove("hidden");

    let target_tweet = {
        "tweet_id" : targetTweet.querySelector("input[name='tweet_id']").value,
        "tweet_text" : targetTweet.querySelector(".tweet_text").innerHTML,
        "tweet_image_path" : targetTweet.querySelector("input[name='tweet_image_path']").value,
        "profile_picture_path" : targetTweet.querySelector(".user_profile_picture").getAttribute('src')
    }

    // CREATE UPDATE TWEET ELEMENT
    edit_tweet_form.querySelector(".tweet_text").value = target_tweet["tweet_text"];
    edit_tweet_form.querySelector("input[name='tweet_id']").value = target_tweet["tweet_id"];
    edit_tweet_form.querySelector(".user_profile_picture").src = `${target_tweet["profile_picture_path"]}`;

    // // CHECK IF TWEET INCLUDES AN IMAGE
    if (target_tweet["tweet_image_path"] && target_tweet["tweet_image_path"] !== "0"){
        edit_tweet_form.querySelector(".tweet_image_tag").src = `../images/tweet_images/${target_tweet["tweet_image_path"]}`
        edit_tweet_form.querySelector("input[name='tweet_image_path']").value = target_tweet["tweet_image_path"];
        edit_tweet_form.querySelector(".tweet_image_tag").classList.remove("hidden")
        edit_tweet_form.querySelector(".filename").textContent = "Do you want to change the image?"
    } else {
        edit_tweet_form.querySelector(".filename").textContent = ""
        edit_tweet_form.querySelector(".checkmark").classList.add("hidden")
    }
}

////////////////////////////////
// UPDATE TWEET
export default async function updateTweet(event){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/update-tweet/${tweet_id}`, {
        method : "PUT",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        console.log("could not tweet")
        return;
    };

    const response = await connection.json();

    if (response.error === "not an image file"){
        const ErrorInputElement = form.querySelector(".file_upload_icon");
        const errorMessage = "Filetypes allowed: jpg, jpeg, png, heic";
        backendErrorsValidation(ErrorInputElement, errorMessage, "file");
        return;
    }

    // SUCESS
    const updated_tweet = response;

    // DEFINE ELEMENTS TO MANIPULATE DOM
    const edited_tweet_element = document.querySelector(`.tweet-${tweet_id}`)
    const tweet_image_element = form.querySelector("input[name='tweet_image_path']");

    // CONVERT TWEET_UDPATED_AT (EPOCH) TO DATETIME
    let timestamp = updated_tweet.tweet_updated_at;

    edited_tweet_element.querySelector(".tweet_text").innerHTML = updated_tweet.tweet_text;

    // DEFINE IF TWEET INCLUDES AN IMAGE BEFORE UPDATE
    let doesTweetInculdeImage = true;
    if (!tweet_image_element.value || tweet_image_element.value === "0" || tweet_image_element.value === "None" ) {doesTweetInculdeImage = false}
    
    // DEFINE IF UPDATED TWEET INCLUDES AN IMAGE
    let doesUpdatedTweetInculdeImage = true;
    if (!updated_tweet.tweet_image_path || updated_tweet.tweet_image_path === "0" || updated_tweet.tweet_image_path === "None") {
        doesUpdatedTweetInculdeImage = false
    }

    // ADD IMAGETAG TO DOM IF NOT ALREADY IMAGE IN TWEET    
    if (!doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        const new_image_element = `<img class="tweet_image" src="../images/tweet_images/${updated_tweet.tweet_image_path}" alt="Tweet image value='${updated_tweet.tweet_image_path}'"></img>`
        edited_tweet_element.querySelector(".tweet_image_path").insertAdjacentHTML("afterend", new_image_element);
        edited_tweet_element.querySelector(".tweet_image_path").value = updated_tweet.tweet_image_path;
    }

    // CHANGE IMAGE IN TWEET
    if (doesTweetInculdeImage && doesUpdatedTweetInculdeImage){
        edited_tweet_element.querySelector("input[name='tweet_image_path']").value = updated_tweet.tweet_image_path;
        edited_tweet_element.querySelector(".tweet_image").src = `../images/tweet_images/${updated_tweet.tweet_image_path}`;
        tweet_image_element.value = updated_tweet.tweet_image_path;
    }

    closeEditTweet(event)
}

function closeEditTweet(event){
    const edit_tweet_container = document.querySelector(".edit_tweet_container");
    const tweet_id = event.target.closest("#edit-tweet-form").querySelector("input[name=tweet_id]").value;

    document.querySelector(`.tweet-${tweet_id} .button-wrapper-inner`).classList.add("hidden");

    edit_tweet_container.classList.add("hidden");
    edit_tweet_container.querySelector(".tweet_image_tag").classList.add("hidden")
    edit_tweet_container.querySelector(".filename").textContent = ""
    edit_tweet_container.querySelector(".checkmark").classList.add("hidden")
    edit_tweet_container.querySelector(".edit_tweet_bottom .error_message").classList.add("hidden")
    edit_tweet_container.querySelector(".edit_tweet_bottom .error_message").textContent = ""
    edit_tweet_container.querySelector("input['name=tweet_image_path']").value = None;

}