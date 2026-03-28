// main.js — shared JS across all pages

// Sticky nav shadow on scroll (home page)
const nav = document.querySelector('.nav');
if (nav) {
    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
}

// Auto-dismiss flash messages after 4s
document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
        el.style.transition = 'opacity 0.4s ease';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 400);
    }, 4000);
});