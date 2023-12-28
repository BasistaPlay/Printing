const sr = ScrollReveal({
    distance: '100px',
    duration: 2700,
    reset: true,
});

sr.reveal('.hero-text', {delay:200, origin: 'bottom'});
sr.reveal('.top-products-header', {delay:200, origin: 'bottom'});
sr.reveal('#product1', {delay:300, origin: 'bottom'});
sr.reveal('#product2', {delay:400, origin: 'bottom'});
sr.reveal('#product3', {delay:500, origin: 'bottom'});


$(document).ready(function() {
    $(".down-arrow").click(function() {
        $('html, body').animate({
            scrollTop: $(".top-products").offset().top
        }, 1000);
    });
});