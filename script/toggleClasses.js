export {toggleDisplaySignup, toggleDisplayLogin, openViewMoreOptions, closeViewMoreOptions, toggleLogout, toggleLikeButtons, toggleFollowButtons}

////////////////////////////////
// TOGGLE CLASS FUNCTIONS

export default function toggleDisplaySignup(){
    // TOGGLE HIDDEN CLASS ON SIGN UP FORM
    document.querySelector(".signup-form-container").classList.toggle("hidden");
}

function toggleDisplayLogin(){
    // TOGGLE HIDDEN CLASS ON LOGIN FORM
    document.querySelector(".login-form-container").classList.toggle("hidden");
}

function openViewMoreOptions(event){
    // OPEN MORE OPTIONS POPUP
    event.target.nextElementSibling.classList.remove("hidden");
}

function closeViewMoreOptions(event){
    // CLOSE MORE OPTIONS POPUP
    event.target.closest(".button-wrapper-inner").classList.add("hidden");
}

function toggleLikeButtons(form){
    // TOGGLE HIDDEN CLASS ON LIKE BUTTONS
    form.querySelector(".like-button").classList.toggle("hidden")
    form.querySelector(".dislike-button").classList.toggle("hidden")
}

function toggleLogout(){
    // TOGGLE HIDDEN CLASS ON LOGOUT POPUP
    document.querySelector(".logout-wrapper").classList.toggle("hidden")
}

function toggleFollowButtons(form){
    // TOGGLE HIDDEN CLASS ON FOLLOW BUTTONS
    form.querySelector(".follow-button").classList.toggle("hidden")
    form.querySelector(".unfollow-button").classList.toggle("hidden")
}
