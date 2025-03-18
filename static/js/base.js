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

document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('dropdownButton');
    const menu = document.getElementById('dropdownMenu');

    button.addEventListener('click', function () {
        // Toggle the visibility of the dropdown menu
        menu.classList.toggle('hidden');
    });

    // Close the dropdown menu if clicked outside of it
    window.addEventListener('click', function (event) {
        if (!button.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.add('hidden');
        }
    });
});

document.querySelector('.dropdown button').addEventListener('click', function() {
    const content = document.querySelector('.dropdown-content');
    content.classList.toggle('hidden');
});

document.addEventListener('click', function(event) {
    const target = event.target;
    if (!target.closest('.dropdown')) {
        document.querySelector('.dropdown-content').classList.add('hidden');
    }
});

document.addEventListener('contextmenu', function(event) {
    if (event.target.classList.contains('no-search')) {
        event.preventDefault();
    }
});

document.querySelectorAll('.no-search').forEach(img => {
    img.addEventListener('dragstart', event => event.preventDefault());
    img.addEventListener('mousedown', event => event.preventDefault());
});

document.querySelectorAll('.draggable').forEach(img => {
    img.setAttribute('draggable', 'true');
});