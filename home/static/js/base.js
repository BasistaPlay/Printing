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

let navlist = document.querySelector('.navlist')

const menuIconSvg = document.getElementById('menu-icon-svg');
const closeIconSvg = document.getElementById('close-icon-svg');
const menuIconDiv = document.getElementById('menu-icon');

menuIconDiv.addEventListener('click', () => {

    if (menuIconSvg.style.display !== 'none') {

        menuIconSvg.style.display = 'none';
        closeIconSvg.style.display = 'block';
    } else {

        menuIconSvg.style.display = 'block';
        closeIconSvg.style.display = 'none';
    }
    navlist.classList.toggle('open')
});
localStorage.setItem('currentSide', 'front');

setTimeout(function() {
    var messages = document.getElementsByClassName('messages');
    for (var i = 0; i < messages.length; i++) {
        (function(message) {
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 1000); // 1 second after opacity change
        })(messages[i]);
    }
}, 5000);