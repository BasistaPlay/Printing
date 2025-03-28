function showLoader() {
    document.getElementById('custom-loader').classList.remove('invisible', 'opacity-0');
    document.getElementById('custom-loader').classList.add('opacity-100');
  }

  function hideLoader() {
    const loader = document.getElementById('custom-loader');
    loader.classList.remove('opacity-100');
    loader.classList.add('opacity-0');
    setTimeout(() => loader.classList.add('invisible'), 300);
  }

    barba.init({
    transitions: [{
      name: 'ericprint-tailwind-loader',
      leave({ current }) {
        showLoader();
        return gsap.to(current.container, { opacity: 0, duration: 0.3 });
      },
      enter({ next }) {
        gsap.set(next.container, { opacity: 0 });
      },
      afterEnter({ next }) {
        return new Promise(resolve => {
          const images = next.container.querySelectorAll('img');
          let loaded = 0;
          const checkLoad = () => {
            loaded++;
            if (loaded === images.length || images.length === 0) {
              gsap.to(next.container, { opacity: 1, duration: 0.3 });
              hideLoader();
              resolve();
            }
          };
          if(images.length === 0) checkLoad();
          images.forEach(img => {
            if (img.complete) checkLoad();
            else img.onload = img.onerror = checkLoad;
          });
        });
      }
    }]
  });
