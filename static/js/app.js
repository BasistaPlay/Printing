let deferredPrompt;
import Cookies from "https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.mjs";

window.addEventListener('beforeinstallprompt', (event) => {
    if (window.matchMedia("(max-width: 768px)").matches && !Cookies.get('installBannerClosed')) {
        event.preventDefault();
        deferredPrompt = event;
        const banner = document.getElementById('install-banner');
        if (banner) {
            banner.style.display = 'block';
        }
    }
});

window.addEventListener('DOMContentLoaded', () => {
    const installBanner = document.getElementById('install-banner');
    const installBtn = document.getElementById('install-btn');
    const closeBtn = document.getElementById('close-btn');
    const closeBtnIOS = document.getElementById('close-btn-ios');
    const iosInstallBanner = document.getElementById('ios-install-banner');

    if (installBanner && installBtn) {
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt = null;
                installBanner.style.display = 'none';
            }
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', (event) => {
            event.stopPropagation();
            installBanner.style.display = 'none';
            Cookies.set('installBannerClosed', 'true', { expires: 30 });
        });
    }

    if (closeBtnIOS) {
        closeBtnIOS.addEventListener('click', (event) => {
            event.stopPropagation();
            iosInstallBanner.style.display = 'none';
            Cookies.set('installBannerClosed', 'true', { expires: 30 });
        });
    }

    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
                  (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const isInStandaloneMode = ('standalone' in window.navigator) && window.navigator.standalone;

    if (isIOS && !isInStandaloneMode && !Cookies.get('installBannerClosed')) {
        if (iosInstallBanner) {
            iosInstallBanner.style.display = 'block';
        }
    }
});
