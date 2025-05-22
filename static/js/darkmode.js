import gsap from 'gsap';

function updateDarkModeIcon(isDark) {
    const darkmodeBtn = document.querySelector('#darkmode');
    if (!darkmodeBtn) return;
    const svgIcon = darkmodeBtn.querySelector('use');
    if (!svgIcon) return;
    svgIcon.setAttribute(
        'xlink:href',
        isDark ? '/static/svg/sprite.svg#sun' : '/static/svg/sprite.svg#moon-ico'
    );
}

function initializeDarkMode() {
    const body = document.body;
    const savedMode = localStorage.getItem('darkMode');
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedMode === 'true' || (savedMode === null && prefersDarkMode)) {
        body.classList.add('dark');
        updateDarkModeIcon(true);
    } else {
        body.classList.remove('dark');
        updateDarkModeIcon(false);
    }

    // Poga uzspiešana
    document.body.addEventListener('click', (event) => {
        const darkmodeBtn = event.target.closest('#darkmode');
        if (!darkmodeBtn) return;

        body.classList.toggle('dark');

        const isDark = body.classList.contains('dark');
        localStorage.setItem('darkMode', isDark ? 'true' : 'false');
        updateDarkModeIcon(isDark);
    });

    // Reaģē uz OS režīma maiņu
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (event) => {
        if (localStorage.getItem('darkMode') === null) {
            body.classList.toggle('dark', event.matches);
            updateDarkModeIcon(event.matches);
        }
    });
}

document.addEventListener('DOMContentLoaded', initializeDarkMode);
