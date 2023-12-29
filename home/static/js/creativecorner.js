const sr = ScrollReveal({
    distance: '100px',
    duration: 2700,
    reset: true,
});

sr.reveal('.container', {delay:500, origin: 'bottom'});

function showSection(sectionId) {
    // Paslēpj visas sadaļas
    var sections = document.querySelectorAll('.shop');
    sections.forEach(function (section) {
        section.classList.remove('active');
    });

    // Paslēpj visas pogas
    var buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(function (button) {
        button.classList.remove('active');
    });

    // Parāda izvēlēto sadaļu
    var selectedSection = document.getElementById(sectionId + '-section');
    selectedSection.classList.add('active');

    // Norāda aktīvo pogu
    var selectedButton = document.getElementById(sectionId + '-btn');
    selectedButton.classList.add('active');
}


var tabButtons = document.querySelectorAll('.tab-buttons button');

tabButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var sectionId = this.dataset.target;
        showSection(sectionId);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const starWrapper = document.querySelector('.star-wrapper');
    const rating = parseFloat(starWrapper.getAttribute('data-rating'));
    const stars = starWrapper.querySelectorAll('.fas');

    stars.forEach(function (star, index) {
        const starValue = index + 1;
        const reversedStarValue = stars.length - starValue + 1;

        if (reversedStarValue <= rating) {
            star.classList.add('active');
        } else if (reversedStarValue - 0.5 === rating) {
            star.classList.add('active-half');
        }
    });
});


