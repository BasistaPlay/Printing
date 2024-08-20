// Eksportējiet addToCart funkciju
function AddToCart(design_id) {
    let numValue = $('.num').text();
    let productCard = $('.product-card[data-product-id]');
    let product_id = productCard.data('product-id');

    var formData = new FormData();
    formData.append('design_id', design_id);
    formData.append('product_id', product_id);
    formData.append('quantity', numValue);

    $.ajax({
        type: 'POST',
        url: '/cart/add/' + design_id + '/',
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
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
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

