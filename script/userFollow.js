export {createFollow, deleteFollow}
import {toggleFollowButtons} from "./toggleClasses.js"

////////////////////////////////
// CREATE FOLLOW
export default async function createFollow(event){
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
async function deleteFollow(event){
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
