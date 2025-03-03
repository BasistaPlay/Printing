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
            if (response.success) {
                showMessages(response.messages);
                var cartCountElement = $('#cart-count');
                if (cartCountElement.length === 0) {
                    var newCartCountElement = $('<span id="cart-count"></span>');
                    newCartCountElement.text(response.cart_count);
                    $('#cart').append(newCartCountElement);
                } else {
                    cartCountElement.text(response.cart_count);
                }
            } else {
                showMessages(response.messages);
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
            showMessages(['Radās kļūda, mēģinot pievienot preci.']);
        }
    });
}

function showMessages(messages) {
    const messageContainer = $('.message-container');

    messageContainer.empty();

    messages.forEach(message => {
        const div = $('<div></div>').addClass('alert alert-success').text(message);

        if (message.includes('Prece veiksmīgi pievienota grozam')) {
            div.addClass('alert-success');
        } else if (message.includes('Prece nav atrasta')) {
            div.addClass('alert-danger');
        }

        messageContainer.append(div);

        setTimeout(() => {
            div.fadeOut(300, function() { $(this).remove(); });
        }, 3000);
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
