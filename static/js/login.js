// Home button redirection
document.getElementById('home').onclick = function() {
    location.href = '/';
}

// Forgot password button functionality
document.getElementById('forgot-password').onclick = function() {
    document.getElementById('forgot-password-modal').style.display = 'block';
}

// Close the modal
document.querySelector('.close').onclick = function() {
    document.getElementById('forgot-password-modal').style.display = 'none';
}

// Send email for forgot password
document.getElementById('send-email').onclick = function() {
    var email = document.getElementById('forgot-password-email').value;
    if (email) {
        alert("Your password and username have been sent to your email.");
        document.getElementById('forgot-password-modal').style.display = 'none';
    } else {
        alert("Please enter a valid email address.");
    }
}

// Close the modal if clicked outside
window.onclick = function(event) {
    var modal = document.getElementById('forgot-password-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
