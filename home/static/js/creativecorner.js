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

    document.querySelectorAll('.color-option').forEach(function(colorOption) {
        colorOption.addEventListener('click', function() {
            this.classList.toggle('active');
    
            var selectedColors = [];
            document.querySelectorAll('.color-option.active').forEach(function(activeColor) {
                selectedColors.push(activeColor.getAttribute('data-color-id'));
            });
            document.getElementById('selected-colors').value = selectedColors.join(' ');
    
            performAjaxRequest();
            updateColorIcons()
        });
    });

    var $form = $('#filter-form');
    var $searchInput = $('#search-input');
    var $productSelect = $('#product-select');

    $form.on('submit', function(event) {
        event.preventDefault();

        performAjaxRequest();
    });

    $searchInput.on('keyup', function() {
        performAjaxRequest();
    });

    $productSelect.on('change', function() {
        performAjaxRequest();
    });

    $(document).on('click', '.pagination a', function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        var formData = $form.serialize();

        $.ajax({
            type: 'GET',
            url: url,
            data: formData,
            success: function(response) {
                var newContent = $(response);
                $('.container').html(newContent.find('.container').html());
                $('.pagination').html(newContent.find('.pagination').html());

                updateStars();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });

    function performAjaxRequest() {
        var formData = $form.serialize();

        $.ajax({
            type: 'GET',
            url: '/creative-corner/',
            data: formData,
            success: function(response) {
                var newContent = $(response);
                $('.container').html(newContent.find('.container').html());
                $('.pagination').html(newContent.find('.pagination').html());

                updateStars();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    }
});

function updateColorIcons() {
    document.querySelectorAll('.color-option').forEach(function(colorOption) {
        var isActive = colorOption.classList.contains('active');
        var icon = colorOption.querySelector('.check-icon');

        if (!icon) {
            icon = document.createElement('i');
            icon.className = 'fas fa-check check-icon';
            colorOption.appendChild(icon);
        }

        icon.style.display = isActive ? 'block' : 'none';
        
        icon.style.color = isActive ? '#23FF0E' : 'transparent';
        icon.style.fontSize  = '10px';
        icon.style.textAlign  = 'center';
        icon.style.marginTop  = '3px';

    });
}

var previousScrollPosition = 0;

// Atjaunina paginācijas joslu atkarībā no lapas skrolēšanas
window.addEventListener('scroll', function() {
  var currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
  var windowHeight = window.innerHeight;

  // Ja esam virs lapas augšējās daļas vai skrolējam uz augšu, pārvietojam joslu uz apakšu
  if (currentScrollPosition < previousScrollPosition || currentScrollPosition < windowHeight) {
    document.querySelector('.pagination').style.bottom = '0';
  } else {
    // Ja esam zem lapas augšējās daļas un skrolējam uz leju, pārvietojam joslu uz augšu
    document.querySelector('.pagination').style.bottom = '-60px';
  }

  // Atjauno iepriekšējo skrollēšanas pozīciju
  previousScrollPosition = currentScrollPosition;
});

var isAddingToCart = false;

function AddToCart(order_id) {
    if (!isAddingToCart) {
        isAddingToCart = true;
        var formData = new FormData();
        formData.append('product_id', order_id);

        $.ajax({
            type: 'POST',
            url: '/cart/add/' + order_id + '/',
            data: formData,
            contentType: false,
            processData: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function(response) {
                console.log(response);
                displaySuccessMessage('Product added to cart successfully!');
                var cartCountElement = $('#cart-count');
                if (cartCountElement.length === 0) {
                    var newCartCountElement = $('<span id="cart-count"></span>');
                    newCartCountElement.text(response.cart_count);
                    $('#cart').append(newCartCountElement);
                } else {
                    cartCountElement.text(response.cart_count);
                }
                isAddingToCart = false;
            },
            error: function(xhr, status, error) {
                console.error(error);
                isAddingToCart = false;
            }
        });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function displaySuccessMessage(message) {
    $('#success-message').text(message);
    $('#success-message').fadeIn();
    
    setTimeout(function() {
        $('#success-message').fadeOut();
    }, 5000);
}