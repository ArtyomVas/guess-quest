// riddle.js

// Get the overlay and buttons
var overlay = document.getElementById("overlay");
var notNowButton = document.getElementById("not-now");
var startButton = document.getElementById("start");

// "Not now" button redirection
notNowButton.onclick = function() {
    location.href = '/';
}

// "Start" button functionality
startButton.onclick = function() {
    overlay.style.display = "none";
}

// "Give up" button functionality
document.getElementById('give-up').onclick = function() {
    alert('Keep trying! You can do it!');
}
