import {clickEventHandlers, inputEventHandlers, submitEventHandlers, onChangeEventHandlers} from "./eventHandlers.js";

window.addEventListener('DOMContentLoaded', () => {
    init();
});

function init(){
    clickEventHandlers();
    submitEventHandlers();
    onChangeEventHandlers();

    inputEventHandlers(document.querySelectorAll(".signup-form input"), "all");
    inputEventHandlers(document.querySelectorAll(".login-form input"), "all");
    inputEventHandlers(document.querySelectorAll(".post_tweet-wrapper textarea"), "one");
    inputEventHandlers(document.querySelectorAll(".edit_tweet textarea"), "one");
}
