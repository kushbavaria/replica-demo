const button = document.querySelector("button");
const form = document.querySelector("form");

function validateForm() {
    let user = form["user"].value;
    let password = form["password"].value;
    if (user === '' || password === '') {
        alert("Please enter valid username and password");
        return false;
    }
}