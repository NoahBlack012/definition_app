var num_questions;
var answers_correct = 0; 

async function get_quiz_data(topic) {
    const res = await fetch(`base/get_quiz_data/${topic}`)
    const data = await res.json();  
    return data;
}

get_quiz_data(document.URL).then(data => {
    var quiz_data = data
})

document.addEventListener("DOMContentLoaded", () => {
    console.log(quiz_data);
})