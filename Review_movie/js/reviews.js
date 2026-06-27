const reviewsContainer =
document.getElementById("reviewsContainer");

let reviews =
JSON.parse(localStorage.getItem("reviews")) || [];

function displayReviews(){

    reviewsContainer.innerHTML = "";

    if(reviews.length === 0){

        reviewsContainer.innerHTML = `
        <div class="no-reviews">
            No reviews submitted yet.
        </div>
        `;

        return;
    }

    reviews.forEach((review,index)=>{

        reviewsContainer.innerHTML += `

        <div class="review-card">

            <h2>${review.movie}</h2>

            <div class="review-rating">
                ⭐ Your Rating:
                <strong>${review.rating}/10</strong>
            </div>

            <div class="review-text">
                ${review.review}
            </div>

            <button
                class="delete-btn"
                onclick="deleteReview(${index})">
                Delete Review
            </button>

        </div>

        `;

    });

}

function deleteReview(index){

    reviews.splice(index,1);

    localStorage.setItem(
        "reviews",
        JSON.stringify(reviews)
    );

    displayReviews();
}

displayReviews();