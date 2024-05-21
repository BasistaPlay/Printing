const sr = ScrollReveal({
    distance: '100px',
    duration: 2700,
    reset: true,
});

sr.reveal('.hero-text', {delay:200, origin: 'bottom'});
sr.reveal('.top-products-header', {delay:200, origin: 'bottom'});
sr.reveal('.pricing', {delay:200, origin: 'bottom'});
sr.reveal('#product1', {delay:300, origin: 'bottom'});
sr.reveal('#product2', {delay:400, origin: 'bottom'});
sr.reveal('#product3', {delay:500, origin: 'bottom'});


$(document).ready(function() {
    $(".down-arrow").click(function() {
        $('html, body').animate({
            scrollTop: 740
        }, 1000);
    });
});

$(document).ready(function() {
    $(".second").click(function() {
        $('html, body').animate({
            scrollTop: 1400 
        }, 1000);
    });
});


$(document).ready(function() {
    $(".third").click(function() {
        $('html, body').animate({
            scrollTop: 0 
        }, 1000);
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const particles = document.querySelector(".particles");

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement("span");
        const angle = Math.random() * 2 * Math.PI;
        const radius = Math.random() * 80 + 80;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        particle.style.setProperty("--x", x);
        particle.style.setProperty("--y", y);
        particle.style.animationDelay = `${Math.random() * 3}s`;

        particles.appendChild(particle);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    if (window.location.href.indexOf("http://127.0.0.1:8000/success/") !== -1) {
        document.querySelector(".order-confirmation").style.display = "block";
    }
});