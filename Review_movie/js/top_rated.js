const modal = document.getElementById("reviewModal");
const closeModal = document.getElementById("closeModal");
const movieTitle = document.getElementById("movieTitle");
const movieRating = document.getElementById("movieRating");
const reviewText = document.getElementById("reviewText");
const userRating = document.getElementById("userRating");
const submitReview = document.getElementById("submitReview");

let selectedMovie = "";

document.querySelectorAll(".movie-card").forEach(card => {

    card.addEventListener("click", () => {

        selectedMovie = card.dataset.movie;

        movieTitle.textContent = selectedMovie;
        movieRating.textContent = card.dataset.rating;

        reviewText.value = "";
        userRating.value = "10";

        modal.classList.add("show");

    });

});

closeModal.onclick = () => modal.classList.remove("show");

window.onclick = (e) => {

    if (e.target === modal) {
        modal.classList.remove("show");
    }

};

document.addEventListener("keydown", e => {

    if (e.key === "Escape") {
        modal.classList.remove("show");
    }

});

submitReview.onclick = () => {

    const review = reviewText.value.trim();

    if (!review) {
        alert("Please write a review.");
        return;
    }

    const reviews = JSON.parse(localStorage.getItem("movieReviews")) || [];

    reviews.push({
        movie: selectedMovie,
        rating: userRating.value,
        review: review,
        date: new Date().toLocaleString()
    });

    localStorage.setItem("movieReviews", JSON.stringify(reviews));

    alert("Review Submitted!");

    modal.classList.remove("show");

};