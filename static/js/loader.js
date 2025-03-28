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
      const namespace = next.container.dataset.barbaNamespace;

      switch (namespace) {
        case 'design':
          if (typeof initDesignPage === 'function') initDesignPage();
          break;
        case 'homepage':
          if (typeof initHomePage === 'function') initHomePage();
          break;
      }

      const container = next.container;

      const onFullyLoaded = () => {
        requestAnimationFrame(() => {
          gsap.to(container, { opacity: 1, duration: 0.3 });
          hideLoader();
        });
      };

      if (document.readyState === 'complete') {
        onFullyLoaded();
      } else {
        window.addEventListener('load', onFullyLoaded);
      }
    }
  }]
});
