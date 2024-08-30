let darkmode = document.querySelector('#darkmode');
let body = document.body;
let svgIcon = darkmode.querySelector('use');

// Pārbaudīt, vai ir saglabāts iepriekšējais dark mode stāvoklis
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// Ja ir saglabāts, tad uzstādīt dark mode
if (isDarkMode) {
    svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
    body.classList.add('dark');
}

darkmode.onclick = () => {
    if (body.classList.contains('dark')) {
        // Pārslēgt uz light mode
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#moon-ico');
        body.classList.remove('dark');
        localStorage.setItem('darkMode', 'false');
    } else {
        // Pārslēgt uz dark mode
        svgIcon.setAttribute('xlink:href', '/static/svg/sprite.svg#sun');
        body.classList.add('dark');
        localStorage.setItem('darkMode', 'true');
    }
}