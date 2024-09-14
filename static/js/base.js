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