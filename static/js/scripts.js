// scripts.js

document.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});
window.addEventListener('scroll', function() {
    const video = document.getElementById('background-video');
    let scrollPosition = window.scrollY;
    video.style.filter = `blur(${scrollPosition / 50}px)`;
});
