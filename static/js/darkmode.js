let body = document.body;

function updateDarkModeIcon(isDark) {
    let darkmodeBtn = document.querySelector('#darkmode');
    if (!darkmodeBtn) return;
    let svgIcon = darkmodeBtn.querySelector('use');
    if (isDark) {
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
    } else {
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#moon-ico');
    }
}

function initializeDarkMode() {
    let savedMode = localStorage.getItem('darkMode');
    let prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedMode === 'true' || (savedMode === null && prefersDarkMode)) {
        body.classList.add('dark');
        updateDarkModeIcon(true);
    } else {
        body.classList.remove('dark');
        updateDarkModeIcon(false);
    }
}

initializeDarkMode();

document.body.addEventListener('click', (event) => {
    let darkmodeBtn = event.target.closest('#darkmode');
    if (!darkmodeBtn) return;

    body.classList.toggle('dark');

    let isDark = body.classList.contains('dark');
    localStorage.setItem('darkMode', isDark ? 'true' : 'false');
    updateDarkModeIcon(isDark);
});

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (localStorage.getItem('darkMode') === null) {
        body.classList.toggle('dark', event.matches);
        updateDarkModeIcon(event.matches);
    }
});

barba.hooks.after(() => {
    let isDark = body.classList.contains('dark');
    updateDarkModeIcon(isDark);
});
