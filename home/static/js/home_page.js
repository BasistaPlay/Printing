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
