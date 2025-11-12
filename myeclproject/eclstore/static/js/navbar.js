
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');

navToggle.addEventListener('click', () => {
navLinks.classList.toggle('show');
navToggle.classList.toggle('active');
});
