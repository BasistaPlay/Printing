
let darkmode = document.querySelector('#darkmode');
let body = document.body;

// Pārbaudīt, vai ir saglabāts iepriekšējais dark mode stāvoklis
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// Ja ir saglabāts, tad uzstādīt dark mode
if (isDarkMode) {
    darkmode.classList.replace('bx-moon', 'bx-sun');
    body.classList.add('dark');
}

darkmode.onclick = () => {
    if (darkmode.classList.contains('bx-moon')) {
        darkmode.classList.replace('bx-moon', 'bx-sun');
        body.classList.add('dark');
        // Saglabāt dark mode stāvokli
        localStorage.setItem('darkMode', 'true');
    } else {
        darkmode.classList.replace('bx-sun', 'bx-moon');
        body.classList.remove('dark');
        // Saglabāt light mode stāvokli
        localStorage.setItem('darkMode', 'false');
    }
}

let menu = document.querySelector('#menu-icon')
let navlist = document.querySelector('.navlist')

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('open')
}
