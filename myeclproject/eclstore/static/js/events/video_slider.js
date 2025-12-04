document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector(".video-slider");
    const nextBtn = document.querySelector(".video-next");
    const prevBtn = document.querySelector(".video-prev");

    if (!slider) return;

    const scrollAmount = 380;

    nextBtn.addEventListener("click", () => {
        slider.scrollBy({ left: scrollAmount, behavior: "smooth" });
    });

    prevBtn.addEventListener("click", () => {
        slider.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    });
});
