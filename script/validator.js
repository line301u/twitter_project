export {validate, backendErrorsValidation, clear_validate_error}

function _all(q, e=document){return e.querySelectorAll(q)}
function _one(q, e=document){return e.querySelector(q)}

////////////////////////////////
// VALIDATE FORM
export default function validate(event, callback){
    const form = event.target

    _all("[data-validate]",form).forEach(function(element){ 
        element.classList.remove("validate_error")
        element.style.backgroundColor = "white"
    })
    _all("[data-validate]",form).forEach( function(element){
        switch(element.getAttribute("data-validate")){
        case "str":
            if( element.value.length < parseInt(element.getAttribute("data-min"))){
                let inputType = element.getAttribute('data-input-type')
                element.nextElementSibling.textContent = `${inputType} is missing`
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
            if (element.value.length > parseInt(element.getAttribute("data-max"))){
                let inputType = element.getAttribute('data-input-type')
                element.nextElementSibling.textContent = `${inputType} is missing`
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }

        break;
        case "int":
            if( ! /^\d+$/.test(element.value)  ||
                parseInt(element.value) < parseInt(element.getAttribute("data-min")) || 
                parseInt(element.value) > parseInt(element.getAttribute("data-max"))
            ){
            element.classList.add("validate_error")
            }
        break;      
        case "email":
            let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if( ! re.test(element.value.toLowerCase()) ){
                element.nextElementSibling.textContent = "Email is not valid"
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
            if( element.value.length < parseInt(element.getAttribute("data-min"))){
                element.nextElementSibling.textContent = "Email is missing"
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
            if (element.value.length > parseInt(element.getAttribute("data-max"))){
                element.nextElementSibling.textContent = "Email is too long"
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
        break;
        case "password":
            if( element.value.length < parseInt(element.getAttribute("data-min"))){
                element.nextElementSibling.textContent = "Password is too short"
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
            if (element.value.length > parseInt(element.getAttribute("data-max"))){
                element.nextElementSibling.textContent = "Password is too long"
                element.nextElementSibling.classList.remove("hidden")
                element.classList.add("validate_error")
                if (element.closest(".input_group")){
                    element.closest(".input_group").style.marginBottom = "1rem"
                }
            }
        break;
        case "re":       
            var regex = new RegExp(element.getAttribute("data-re"));
            if( ! regex.test(element.value) ){
            element.classList.add("validate_error")
            }
        break;
        case "match":
            if( element.value != _one(`[name='${element.getAttribute("data-match-name")}']`, form).value ){
            element.classList.add("validate_error")
            }
        break;
        }
    })

    if( ! _one(".validate_error", form) ){ callback(event); return }

    }

////////////////////////////////
// SHOW ERRORS DATABASE RESPONSE
function backendErrorsValidation(element, errorMessage, elementType){
    element.nextElementSibling.textContent = errorMessage;
    element.nextElementSibling.classList.remove("hidden");

    if (elementType !== "file"){
        element.classList.add("validate_error");
    }

    if (element.closest(".input_group")){
        element.closest(".input_group").style.marginBottom = "1rem"
    }
}

////////////////////////////////
// CLEAR INPUTS ON KEYUP AFTER ERROR
function clear_validate_error(event){
    if (event.target.classList.contains("validate_error")){
        const element = event.target;
        element.classList.remove("validate_error")
        element.nextElementSibling.textContent = ""
        element.nextElementSibling.classList.add("hidden")
        if (element.closest(".input_group")){
            element.closest(".input_group").style.marginBottom = "0rem"
        }
    }
}

