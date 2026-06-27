const modal = document.getElementById("reviewModal");

const closeBtn = document.getElementById("closeModal");

const movieTitle = document.getElementById("movieTitle");

const movieRating = document.getElementById("movieRating");

const submitBtn = document.getElementById("submitReview");

const reviewText = document.getElementById("reviewText");

const userRating = document.getElementById("userRating");

let selectedMovie = "";

// Open Modal

document.querySelectorAll(".movie-card").forEach(card=>{

    card.addEventListener("click",()=>{

        selectedMovie = card.dataset.movie;

        movieTitle.textContent = selectedMovie;

        movieRating.textContent = card.dataset.rating;

        reviewText.value = "";

        userRating.value = "10";

        modal.classList.add("show");

    });

});

// Close

closeBtn.onclick=()=>{

    modal.classList.remove("show");

};

window.onclick=(e)=>{

    if(e.target===modal){

        modal.classList.remove("show");

    }

};

// Submit Review

submitBtn.onclick=()=>{

    const review=reviewText.value.trim();

    const rating=userRating.value;

    if(review===""){

        alert("Please write a review.");

        return;

    }

    let reviews=JSON.parse(localStorage.getItem("movieReviews"))||[];

    reviews.push({

        movie:selectedMovie,

        rating:rating,

        review:review,

        date:new Date().toLocaleString()

    });

    localStorage.setItem("movieReviews",JSON.stringify(reviews));

    alert("Review Submitted Successfully!");

    modal.classList.remove("show");

};

// ESC Close

document.addEventListener("keydown",(e)=>{

    if(e.key==="Escape"){

        modal.classList.remove("show");

    }

});