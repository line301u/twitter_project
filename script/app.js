window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
});

async function createUser(){
    const form = event.target.form;

    const connection = await fetch("/signup", {
        method : "POST",
        body : new FormData(form)
    });

    console.log(connection.ok)
    if (!connection.ok){
        console.log("connection failed")
        alert("could not sign up")
    }

    // CLEAR INPUT FIELDS IN FORM
    allFormInputs = form.querySelectorAll("input");
    allFormInputs.forEach(input => {
        input.value = "";
    });
}

async function postTweet(){
    const form = event.target.form;
    const connection = await fetch("/tweet", {
        method: "POST",
        body: new FormData(form)
    });

    tweet = await connection.json();

    if (!connection.ok){
        console.log("connection failed")
        alert("could not tweet")
    };

    displayTweet(tweet);

    form.querySelector("#image_upload").value = "";
    form.querySelector(".tweet_text").value = "";
}

async function displayTweet(tweet){
    const container = document.querySelector(".tweets_wrapper");
    const template = document.querySelector('.tweet_template');
    console.log(tweet)

    if ('content' in document.createElement('template')) {
        // CREATE CLONE OF TWEET TEMPLATE
        const clone = template.content.cloneNode(true);

        clone.querySelector("form").classList.add(`tweet-${tweet.tweet_id}`);
        clone.querySelector(".tweet_id").value = tweet.tweet_id;
        clone.querySelector(".user_id").value = tweet.fk_user_id;
        clone.querySelector(".user_profile_picture").src = `../images/user_profile_pictures/${tweet.user_profile_picture_path}`;
        clone.querySelector(".user_first_name").textContent = tweet.user_first_name;
        clone.querySelector(".user_info a").href = `/user/${tweet.fk_user_id}`;

        if (tweet.user_last_name) {
            clone.querySelector(".user_last_name").textContent = tweet.user_last_name;
        }

        clone.querySelector(".tweet_created_at").textContent = ` · ${tweet.tweet_created_at}`;
        clone.querySelector(".user_name").textContent = `@${tweet.user_name}`;
        clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
        clone.querySelector(".tweet_image_path").value = tweet.tweet_image_path;

        if (tweet.tweet_image_path && tweet.tweet_image_path !== "0"){
            clone.querySelector(".tweet_image").src = `../images/tweet_images/${tweet.tweet_image_path}`;
        } else {
            clone.querySelector(".tweet_image").classList.add("hidden")
        }

        container.insertBefore(clone, container.children[0]);
    }
}

////////////////////////////////
// DELETE TWEET
async function deleteTweet(){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/delete-tweet/${tweet_id}`, {
        method : "DELETE"
    });

    // CREATE FAILED
    if(!connection.ok){
        alert("could not delete tweet")
        return;
    };

    // SUCESS
    const response = await connection.text();

    form.remove();
}

////////////////////////////////
// OPEN EDIT TWEET VIEW
function openEditTweet(){
    let targetTweet = event.target.form;
    const edit_tweet_form = document.querySelector(".edit_tweet_container")
    edit_tweet_form.classList.remove("hidden");
    targetTweet.querySelector(".button-wrapper-inner").classList.add("hidden");

    target_tweet = {
        "tweet_id" : targetTweet.querySelector("input[name='tweet_id']").value,
        "tweet_text" : targetTweet.querySelector(".tweet_text").innerHTML,
        "tweet_image_path" : targetTweet.querySelector("input[name='tweet_image_path']").value,
        "profile_picture_path" : targetTweet.querySelector(".user_profile_picture").getAttribute('src')
    }

    console.log(target_tweet)

    // CREATE UPDATE TWEET ELEMENT
    edit_tweet_form.querySelector("input[name='tweet_text']").value = target_tweet["tweet_text"];
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

function cancelEditTweet(){
    let edit_tweet_container = document.querySelector(".edit_tweet_container");
    edit_tweet_container.classList.add("hidden");
    edit_tweet_container.querySelector(".tweet_image_tag").classList.add("hidden")
    edit_tweet_container.querySelector(".filename").textContent = ""
    edit_tweet_container.querySelector(".checkmark").classList.add("hidden")
}

////////////////////////////////
// UPDATE TWEET
async function updateTweet(){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/update-tweet/${tweet_id}`, {
        method : "PUT",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        alert("could not tweet")
        return;
    };

    // SUCESS
    const updated_tweet = await connection.json();
    console.log(updated_tweet)

    // DEFINE ELEMENTS TO MANIPULATE DOM
    const edited_tweet_element = document.querySelector(`.tweet-${tweet_id}`)
    const tweet_image_element = form.querySelector("input[name='tweet_image_path']");

    // CONVERT TWEET_UDPATED_AT (EPOCH) TO DATETIME
    let timestamp = updated_tweet.tweet_updated_at;
    let converted_epoch = covertEpochToDateTime(timestamp);

    edited_tweet_element.querySelector(".tweet_updated_at").innerHTML = converted_epoch;
    edited_tweet_element.querySelector(".tweet_updated_at").classList.remove("hidden")
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

    closeEditTweet()
}

function closeEditTweet(){
    const edit_tweet_container = document.querySelector(".edit_tweet_container");
    edit_tweet_container.classList.add("hidden");
    edit_tweet_container.querySelector(".tweet_image_tag").classList.add("hidden")
    edit_tweet_container.querySelector(".filename").textContent = ""
    edit_tweet_container.querySelector(".checkmark").classList.add("hidden")
}

////////////////////////////////
// CONVERT EPOCH TO DATETIME
function covertEpochToDateTime(timestamp){
    let date = new Date(timestamp * 1000);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2);
    let day = date.getDate();
    let hours = date.getHours();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    let minutes = date.getMinutes();

    return `Last edited: ${hours}:${minutes} ${ampm}, ${day}-${month}-${year}`;
}

////////////////////////////////
// CREATE FOLLOW
async function createFollow(){
    const form = event.target.form;
    const user_id = form.querySelector("input[name='user_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/follow-user/${user_id}`, {
        method: "POST",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        alert("could not tweet")
        return;
    };

    // SUCESS
    const response = await connection.text();

    toggleFollowButtons(form);
}

////////////////////////////////
// DELETE FOLLOW
async function deleteFollow(){
    const form = event.target.form;
    const user_id = form.querySelector("input[name='user_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/unfollow-user/${user_id}`, {
        method : "DELETE",
        body : new FormData(form)
    });

    // CREATE FAILED
    if(!connection.ok){
        alert("could not delete follow")
        return;
    };

    // SUCESS
    const response = await connection.text();

    toggleFollowButtons(form);
}

function toggleFollowButtons(form){
    // TOGGLE HIDDEN CLASS ON FOLLOW BUTTONS
    form.querySelector(".follow-button").classList.toggle("hidden")
    form.querySelector(".unfollow-button").classList.toggle("hidden")
}

function fileUploaded(event){
    // CHECK WHEN FILE IS UPLOADED
    const form = event.target.form;
    let fileName = event.target.files[0].name;
    if(fileName){
        form.querySelector(".checkmark").classList.remove("hidden")
        form.querySelector(".filename").textContent = fileName;
        form.querySelector(".tweet_image_tag").classList.add("hidden");
    }
}

////////////////////////////////
// LIKE TWEET
async function likeTweet(){
    const form = event.target.form;
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/like-tweet/${tweet_id}`, {
        method: "POST",
        body : new FormData(form)
    });

    // REQUEST FAILED
    if(!connection.ok){
        alert("could not tweet")
        return;
    };

    // SUCESS
    const response = await connection.text();
    console.log(response);

    toggleLikeButtons(form);
}

////////////////////////////////
// DISLIKE TWEET
async function dislikeTweet(){
    const form = event.target.form;
    console.log(form)
    const tweet_id = form.querySelector("input[name='tweet_id']").value;

    // CREATE REQUEST
    const connection = await fetch(`/unlike-tweet/${tweet_id}`, {
        method : "DELETE",
        body : new FormData(form)
    });

    // CREATE FAILED
    if(!connection.ok){
        alert("could not delete tweet")
        return;
    };

    // SUCESS
    const response = await connection.text();
    console.log(response);
    
    toggleLikeButtons(form);
}

function toggleLikeButtons(form){
    // TOGGLE HIDDEN CLASS ON LIKE BUTTONS
    form.querySelector(".like-button").classList.toggle("hidden")
    form.querySelector(".dislike-button").classList.toggle("hidden")
}

function openViewMoreOptions(){
    event.target.nextElementSibling.classList.remove("hidden");
}

function closeViewMoreOptions(){
    event.target.closest(".button-wrapper-inner").classList.add("hidden");
}