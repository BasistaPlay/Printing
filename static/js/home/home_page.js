document.addEventListener("DOMContentLoaded", function () {
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