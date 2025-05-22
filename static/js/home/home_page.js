document.addEventListener("DOMContentLoaded", function () {
  const particles = document.querySelector(".particles");

  if (particles) {
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
  }

  const root = document.documentElement;
  const marqueeContent = document.querySelector("ul.marquee-content");

  if (marqueeContent) {
      const marqueeElementsDisplayed = parseInt(
          getComputedStyle(root).getPropertyValue("--marquee-elements-displayed"),
          10
      );

      root.style.setProperty("--marquee-elements", marqueeContent.children.length);

      for (let i = 0; i < marqueeElementsDisplayed; i++) {
          const clone = marqueeContent.children[i]?.cloneNode(true);
          if (clone) marqueeContent.appendChild(clone);
      }
  }
});
