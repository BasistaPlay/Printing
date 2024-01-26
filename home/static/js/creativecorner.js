

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
    const starWrappers = document.querySelectorAll('.star-wrapper');

    starWrappers.forEach(function (starWrapper) {
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
});

