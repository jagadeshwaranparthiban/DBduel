// Correct answers for the quiz
const correctAnswers = ["B", "B", "C", "C", "A", "C", "C", "D", "A", "B", "A", "B", "A", "B", "B"];

// Set timer for 20 minutes (1200000 milliseconds)
const quizTimeLimit = 20* 60 * 1000; // 20 minutes
let timer;
let timeLeft = quizTimeLimit;

function startTimer() {
    // Display the timer
    const timerDisplay = document.getElementById("timer");

    timer = setInterval(function () {
        const minutes = Math.floor(timeLeft / 60000);
        const seconds = Math.floor((timeLeft % 60000) / 1000);
        timerDisplay.textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;

        // Check if there are 5 minutes left or less
        if (timeLeft <= 5 * 60 * 1000 && timeLeft > 0) {
            // Turn the timer red and show an alert
            timerDisplay.style.color = "#FF0800";  // Change the text color to red
            timerDisplay.style.backgroundColor = "#f2dede";  // Light red background
            if (timeLeft === 5 * 60 * 1000) {
                alert("Only 5 minutes left! Hurry up!");
            }
        }

        // Check if the time has run out
        if (timeLeft <= 0) {
            clearInterval(timer); // Stop the timer
            calculateScore(); // Automatically submit the quiz
        } else {
            timeLeft -= 1000; // Decrease time by 1 second
        }
    }, 1000); // Update every second
}

// Function to calculate the score
function calculateScore() {
    let score = 0;

    // Loop through each question
    for (let i = 0; i < correctAnswers.length; i++) {
        const userAnswer = document.querySelector(`input[name="question${i + 1}"]:checked`);

        // Check if the user's answer matches the correct answer
        if (userAnswer && userAnswer.value === correctAnswers[i]) {
            score++;
        }
    }

    // Store the score in localStorage
    localStorage.setItem("quizScore", score);

    // Redirect to the results page
    window.location.href = "result.html";
}

// Start the timer when the page loads
window.onload = function () {
    startTimer();
};
