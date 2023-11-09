const toggleBtn = document.querySelector('#menu-icon')
const DropDownMenu = document.querySelector('.dropdown_menu')

toggleBtn.onclick = () => {
    toggleBtn.classList.toggle('bx-x')
    DropDownMenu.classList.toggle('open')
}

const sr = ScrollReveal({
    distance: '65px',
    duration: 2600,
    reset: true,
});

sr.reveal('.content-text', {delay:200, origin: 'top'});
sr.reveal('.content-img', {delay:1500, origin: 'top'});
