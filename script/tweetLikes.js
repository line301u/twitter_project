export {likeTweet, dislikeTweet}
import {toggleLikeButtons} from "./toggleClasses.js"

////////////////////////////////
// LIKE TWEET
export default async function likeTweet(event){
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
async function dislikeTweet(event){
    const form = event.target.form;
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
