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
    updateStars();

    $(document).ready(function() {
        function applyFilters() {
            $.ajax({
                url: "{% url 'creativecorner' %}",
                data: $('#filter-form').serialize(),
                success: function(data) {
                    $('#product-list').html(data.html);
                }
            });
        }

        $('#filter-button').on('click', function() {
            applyFilters();
        });

        $('#search-input, #product-select').on('input change', function() {
            applyFilters();
        });

        $('.color-option').on('click', function() {
            var selectedColors = [];
            $(this).toggleClass('selected');
            $('.color-option.selected').each(function() {
                selectedColors.push($(this).data('color-id'));
            });
            $('#selected-colors').val(selectedColors.join(' '));
            applyFilters();
        });
    });

    document.querySelectorAll('.rating-filter .star').forEach(function (star) {
        star.addEventListener('click', function () {
            const rating = this.getAttribute('data-rating');
            document.getElementById('selected-rating').value = rating;

            document.querySelectorAll('.rating-filter .star').forEach(function (star) {
                if (parseInt(star.getAttribute('data-rating')) <= rating) {
                    star.classList.add('active');
                } else {
                    star.classList.remove('active');
                }
            });

            performAjaxRequest();
        });
    });
});