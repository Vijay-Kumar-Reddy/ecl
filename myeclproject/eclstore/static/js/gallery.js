
const slides = document.querySelectorAll('.gallery-item');
const next = document.querySelector('.next');
const prev = document.querySelector('.prev');
let index = 0;

function updateSlides() {
slides.forEach(slide => slide.className = 'gallery-item');
const prevIndex = (index - 1 + slides.length) % slides.length;
const nextIndex = (index + 1) % slides.length;

slides[index].classList.add('active');
slides[prevIndex].classList.add('prev');
slides[nextIndex].classList.add('next');
}

next.addEventListener('click', () => {
index = (index + 1) % slides.length;
updateSlides();
});

prev.addEventListener('click', () => {
index = (index - 1 + slides.length) % slides.length;
updateSlides();
});

// Auto-play
setInterval(() => {
index = (index + 1) % slides.length;
updateSlides();
}, 5000);

updateSlides();
