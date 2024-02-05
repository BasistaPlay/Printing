/*----- MENU -----*/
const showMenu = (toggleId,navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}
showMenu('nav-toggle','nav-menu')

/*----- CAMBIO COLORS -----*/
const sizes = document.querySelectorAll('.size__tallas');
const colors = document.querySelectorAll('.sneaker__color');
const sneaker = document.querySelectorAll('.sneaker__img');

function changeSize(){
    sizes.forEach(size => size.classList.remove('active'));
    this.classList.add('active');
}

function changeColor(){
    let primary = this.getAttribute('primary');
    let color = this.getAttribute('color');
    let sneakerColor = document.querySelector(`.sneaker__img[color="${color}"]`);

    colors.forEach(c => c.classList.remove('active'));
    this.classList.add('active');

    document.documentElement.style.setProperty('--primary', primary);

    sneaker.forEach(s => s.classList.remove('shows'));
    sneakerColor.classList.add('shows')
}

sizes.forEach(size => size.addEventListener('click', changeSize));
colors.forEach(c => c.addEventListener('click', changeColor));

document.addEventListener('DOMContentLoaded', function () {
    const starWrapper = document.querySelector('.star-wrapper');
    const rating = parseFloat(starWrapper.getAttribute('data-rating'));
    const stars = starWrapper.querySelectorAll('.fas');

    stars.forEach(function (star, index) {
        const starValue = index + 1;

        if (starValue <= rating) {
            star.classList.add('active');
        } else if (starValue - 0.5 === rating) {
            star.classList.add('active-half');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var starWrapper = document.querySelector('.star-wrapper');
    var stars = starWrapper.querySelectorAll('a');

    starWrapper.addEventListener('mouseover', function (e) {
        var targetStar = e.target;
        var ratingValue = targetStar.getAttribute('data-rating-value');

        for (var i = 0; i < stars.length; i++) {
            stars[i].classList.remove('active');
        }

        for (var i = 0; i < ratingValue; i++) {
            stars[i].classList.add('active');
        }
    });

    starWrapper.addEventListener('mouseout', function () {
        for (var i = 0; i < stars.length; i++) {
            stars[i].classList.remove('active');
        }
    });
});