export {covertEpochToDateTime, fileUploaded}

////////////////////////////////
// CONVERT EPOCH TO DATETIME
export default function covertEpochToDateTime(timestamp){
    let date = new Date(timestamp * 1000);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2);
    let day = date.getDate();
    let hours = date.getHours();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    let minutes = date.getMinutes();

    return `${day}-${month}-${year}`;
}

function fileUploaded(event){
    // CHECK WHEN FILE IS UPLOADED
    const form = event.target.form;
    let fileName = event.target.files[0].name;

    if(fileName){
        form.querySelector(".checkmark").classList.remove("hidden")
        form.querySelector(".filename").textContent = fileName;
        if (form.querySelector(".tweet_image_tag")){
            form.querySelector(".tweet_image_tag").classList.add("hidden");
        }
    
        form.querySelector(".file_error").textContent = "";
        form.querySelector(".file_error").classList.add("hidden");
    }
}