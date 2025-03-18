let darkmode = document.querySelector('#darkmode');
let body = document.body;
let svgIcon = darkmode.querySelector('use');

let savedMode = localStorage.getItem('darkMode');

let prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedMode === 'true' || (savedMode === null && prefersDarkMode)) {
    svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
    body.classList.add('dark');
} else {
    svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#moon-ico');
    body.classList.remove('dark');
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (localStorage.getItem('darkMode') === null) {
        if (event.matches) {
            body.classList.add('dark');
            svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
        } else {
            body.classList.remove('dark');
            svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#moon-ico');
        }
    }
});

darkmode.onclick = () => {
    if (body.classList.contains('dark')) {
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#moon-ico');
        body.classList.remove('dark');
        localStorage.setItem('darkMode', 'false');
    } else {
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
        body.classList.add('dark');
        localStorage.setItem('darkMode', 'true');
    }
};
