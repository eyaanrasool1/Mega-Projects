const cards = document.querySelectorAll(".movie-card");

const modal = document.getElementById("reviewModal");
const closeBtn = document.getElementById("closeModal");

const movieTitle = document.getElementById("movieTitle");
const movieRating = document.getElementById("movieRating");

const userRating = document.getElementById("userRating");
const reviewText = document.getElementById("reviewText");
const submitReview = document.getElementById("submitReview");

let selectedMovie = "";

/* Open Modal */

cards.forEach(card => {

    card.addEventListener("click", () => {

        selectedMovie = card.dataset.movie;

        movieTitle.textContent = card.dataset.movie;
        movieRating.textContent = card.dataset.rating;

        modal.style.display = "flex";
    });

});

/* Close Modal */

closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (e) => {

    if(e.target === modal){
        modal.style.display = "none";
    }

});

/* Save Review */

submitReview.addEventListener("click", () => {

    if(reviewText.value.trim() === ""){

        alert("Please write a review.");
        return;

    }

    const review = {

        movie: selectedMovie,
        rating: userRating.value,
        review: reviewText.value,
        date: new Date().toLocaleDateString()

    };

    let reviews =
        JSON.parse(localStorage.getItem("reviews"))
        || [];

    reviews.push(review);

    localStorage.setItem(
        "reviews",
        JSON.stringify(reviews)
    );

    alert("Review Saved Successfully!");

    reviewText.value = "";
    userRating.value = "10";

    modal.style.display = "none";

});

/* Fade Animation */

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";

        }

    });

});

cards.forEach(card => {

    card.style.opacity = "0";
    card.style.transform = "translateY(40px)";
    card.style.transition = ".6s";

    observer.observe(card);

});