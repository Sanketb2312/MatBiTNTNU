window.addEventListener('DOMContentLoaded', (event) => {
    createStars();
});

function showRatingButtion(id) {

    var button = document.getElementById("rating-"+id);
    if(button.style.display === "none") {
        button.style.display = "initial";
    }
    else {
        button.style.display = "none";
    }
}
