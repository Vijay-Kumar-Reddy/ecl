const track = document.querySelector(".gallery-track");
const slides = document.querySelectorAll(".gallery-item");
const next = document.querySelector(".next");
const prev = document.querySelector(".prev");

let index = 0;

function updateSlide() {
    track.style.transform = `translateX(-${index * 100}%)`;
}

if (next) {
    next.addEventListener("click", () => {
        index = (index + 1) % slides.length;
        updateSlide();
    });
}

if (prev) {
    prev.addEventListener("click", () => {
        index = (index - 1 + slides.length) % slides.length;
        updateSlide();
    });
}

updateSlide();
