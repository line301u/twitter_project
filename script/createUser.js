import {backendErrorsValidation} from "./validator.js"
import {toggleDisplayLogin, toggleDisplaySignup} from "./toggleClasses.js"

////////////////////////////////
// SIGN UP USER
export default async function createUser(event){
    const form = event.target;

    const connection = await fetch("/signup", {
        method : "POST",
        body : new FormData(form)
    });

    const response = await connection.text();

    if (response == "email error"){
        const ErrorInputElement = form.querySelector('[name="user_email"]');
        const errorMessage = "Email already exists";
        backendErrorsValidation(ErrorInputElement, errorMessage);
        return;
    }
    if (response == "username error"){
        const ErrorInputElement = form.querySelector('[name="user_name"]');
        backendErrorsValidation(ErrorInputElement, "Username already exists");
        return;
    }

    if (response === "not an image file"){
        const ErrorInputElement = form.querySelector("#user_profile_picture");
        const errorMessage = "Filetypes allowed: jpg, jpeg, png";
        backendErrorsValidation(ErrorInputElement, errorMessage, "file");
        return;
    }

    if (!connection.ok){
        console.log("connection failed")
        return;
    }

    // CLEAR INPUT FIELDS IN FORM
    const allFormInputs = form.querySelectorAll("input");
    allFormInputs.forEach(input => {
        input.value = "";
    });

    toggleDisplaySignup();
    toggleDisplayLogin();
}

