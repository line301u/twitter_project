export {deleteTweet}

////////////////////////////////
// DELETE TWEET
export default async function deleteTweet(event){
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
