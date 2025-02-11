// Retrieve the score from localStorage
const score = localStorage.getItem("quizScore");

// Display the score in the result page
document.getElementById("totalScore").textContent = score;

// Function to restart the quiz
function restartQuiz() {
    localStorage.removeItem("quizScore");
    window.location.href = "index.html";
}
