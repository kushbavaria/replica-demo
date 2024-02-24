<<<<<<< HEAD
const button = document.querySelector("button");
const form = document.querySelector("form");

function validateForm() {
    let user = form["user"].value;
    let password = form["password"].value;
    if (user === '' || password === '') {
        alert("Please enter valid username and password");
        return false;
    }
=======
const button = document.querySelector("button");
const form = document.querySelector("form");

function validateForm() {
    let user = form["user"].value;
    let password = form["password"].value;
    if (user === '' || password === '') {
        alert("Please enter valid username and password");
        return false;
    }
>>>>>>> bc2d6b3e3812ffdde9b508ccab199bcf52b781fa
}