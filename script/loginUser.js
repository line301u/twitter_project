import {backendErrorsValidation} from "./validator.js"

////////////////////////////////
// LOGIN USER
export default async function loginUser(event){
    const form = event.target;

    const connection = await fetch("/login", {
        method : "POST",
        body : new FormData(form)
    });

    const response = await connection.text();
    
    if (response == "password error"){
        const ErrorInputElement = form.querySelector('[name="user_password"]');
        const errorMessage = "Wrong password";
        backendErrorsValidation(ErrorInputElement, errorMessage);
        return;
    }
    if (response == "email error"){
        const ErrorInputElement = form.querySelector('[name="user_email"]');
        const errorMessage = "There is no account with this email";
        backendErrorsValidation(ErrorInputElement, errorMessage);
        return;
    }

    if (!connection.ok){
        console.log("connection failed")
        return;
    }

    window.location.href = "/home"
}
