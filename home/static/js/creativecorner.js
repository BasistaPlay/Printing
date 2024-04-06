


function updateStars() {
    const starWrappers = document.querySelectorAll('.star-wrapper');
    starWrappers.forEach(function (starWrapper) {
        const rating = parseFloat(starWrapper.getAttribute('data-rating'));
        const stars = starWrapper.querySelectorAll('.fas');

        stars.forEach(function (star, index) {
            const starValue = index + 1;

            if (starValue <= rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    // Pirmā zvaigžņu atjaunināšana, kad lapas HTML tiek ielādēta
    updateStars();

    document.querySelectorAll('.color-option').forEach(function(colorOption) {
        colorOption.addEventListener('click', function() {
            this.classList.toggle('active');
    
            var selectedColors = [];
            document.querySelectorAll('.color-option.active').forEach(function(activeColor) {
                selectedColors.push(activeColor.getAttribute('data-color-id'));
            });
            document.getElementById('selected-colors').value = selectedColors.join(' ');

            performAjaxRequest();
        });
    });

    // Notikumu apstrāde, kad tiek veikta kāda filtrēšanas darbība
    var $form = $('#filter-form');
    var $searchInput = $('#search-input');
    var $productSelect = $('#product-select');

    $form.on('submit', function(event) {
        event.preventDefault(); // novēršam noklusējuma formu iesniegšanu

        performAjaxRequest();
    });

    $searchInput.on('keyup', function() {
        performAjaxRequest();
    });

    $productSelect.on('change', function() {
        performAjaxRequest();
    });

    // AJAX pieprasījuma izpildīšana un jauno zvaigznēšu atjaunināšana
    function performAjaxRequest() {
        var formData = $form.serialize();

        $.ajax({
            type: 'GET',
            url: '/creative-corner/',
            data: formData,
            success: function(response) {
                var newBoxes = $(response).find('.container .box');
                $('.container').html(newBoxes);

                updateStars(); // Jauno zvaigznēšu atjaunināšana
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    }
});