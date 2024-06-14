// login.js

// Home button redirection
document.getElementById('home').onclick = function() {
    location.href = '/';
}

// login button redirection
document.getElementById('login').onclick = function() {
    location.href = '/riddle';
}

// Forgot password button functionality
document.getElementById('forgot-password').onclick = function() {
    var email = prompt("What is your email?");
    if (email) {
        // Assuming a valid email address is entered
        alert("Your password and username have been sent to your email.");
    }
}
