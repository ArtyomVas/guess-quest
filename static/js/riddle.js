document.getElementById('give-up').onclick = function() {
    var confirmGiveUp = confirm("Are you sure you want to give up?");
    if (confirmGiveUp) {
        location.href = '/gave_up';
    }
}

// "Check My Answer" button functionality
document.getElementById('check-answer').onclick = function() {
    var userAnswer = document.getElementById('safe-code').value;

    // Send AJAX request to backend to check the answer
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/check_user_answer", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.correct) {
                location.href = '/finished';
            } else {
                alert('That is not correct. Try again!');
            }
        }
    };

    xhr.send("answer=" + encodeURIComponent(userAnswer));
}
