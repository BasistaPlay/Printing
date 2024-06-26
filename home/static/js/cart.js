
updateTotal();
function updateTotal() {
    var subtotalElement = document.getElementById('subtotal');
    var taxElement = document.getElementById('tax');
    var totalElement = document.getElementById('total');
    var totalElements = document.getElementById('total-price');
    var cuponElement = document.getElementById('shipping');
    var payAmount = document.getElementById('payAmount');

    var totalElementsValue = parseFloat(totalElements.innerText);
    var cuponElement = document.querySelector('.Cupon');

    if (cuponElement) {
        var shippingElement = cuponElement.querySelector('#shipping');
    
        if (shippingElement) {
            var cuponElementValue = parseFloat(shippingElement.innerText);
        } 

    }
    var taxRate = 0.21;
    var taxValue = totalElementsValue * taxRate;
  
    taxElement.innerText = taxValue.toFixed(2);
  
    var subtotalValue = totalElementsValue - taxValue + cuponElementValue;
  
    subtotalElement.innerText = subtotalValue.toFixed(2);
  
    var totalValue = subtotalValue + taxValue;
  
    totalElement.innerText = totalValue.toFixed(2);
    payAmount.innerText = totalValue.toFixed(2);
  }



  document.addEventListener('DOMContentLoaded', function () {
    const validateButton = document.getElementById('validate-button');
    const discountTokenInput = document.getElementById('discount-token');
    const validationResult = document.getElementById('validation-result');
    const subtotalElement = document.getElementById('subtotal');
    const cuponElement = document.querySelector('.Cupon');

    validateButton.addEventListener('click', function () {
        const discountCode = discountTokenInput.value;

        fetch('/check_discount_code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `discount-token=${encodeURIComponent(discountCode)}`
        })
        .then(response => response.json())
        .then(data => {
            handleDiscountCodeResponse(data);
        })
        .catch(error => {
            console.error('Kļūda veicot pieprasījumu:', error);
        });
    });

    function handleDiscountCodeResponse(data) {
        if (data.valid) {
            if (data.quantity !== null && data.quantity > 0) {
                data.quantity -= 1;
                updateQuantityOnServer(data.discountCode, data.quantity);
            }
    
            if (data.isExpired) {
                validationResult.innerHTML = 'Atlaides kods nav derīgs, jo termiņš ir beidzies.';
            } else if (data.isActivated) {
                validationResult.innerHTML = 'Atlaides kods ir derīgs, bet jau ir aktivizēts.';
            } else {
                const currencySymbol = data.type === 'percentage' ? '%' : '€';
                validationResult.innerHTML = `Atlaides kods ir derīgs! Vērtība: ${data.value}${currencySymbol}`;
                
                const discountAmount = calculateDiscountAmount(data.type, data.value, parseFloat(subtotalElement.textContent));
                displayDiscountInformation(discountAmount);
                updateTotal();
            }
        } else {
            validationResult.innerHTML = data.message || 'Ievadītais kods nav derīgs.';
            hideDiscountInformation();
        }
    }

    function calculateDiscountAmount(type, value, subtotal) {
        return type === 'percentage' ? (parseFloat(value) / 100) * subtotal : parseFloat(value);
    }

    function displayDiscountInformation(discountAmount) {
        cuponElement.style.display = 'flex';
        cuponElement.querySelector('#shipping').textContent = -discountAmount.toFixed(2);
    }

    function hideDiscountInformation() {
        cuponElement.style.display = 'none';
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        return parts.length === 2 ? parts.pop().split(';').shift() : null;
    }
});


function limitDigits(input, maxLength) {
    if (input.value.length > maxLength) {
        input.value = input.value.slice(0, maxLength);
    }
}

function formatCardNumber(input) {
    let cardNumber = input.value.replace(/\D/g, '');
    cardNumber = cardNumber.replace(/(\d{4})(?=\d)/g, '€1 ');
    input.value = cardNumber;

    checkCardType(cardNumber);
}


function checkCardType(cardNumber) {
    const cardTypeElement = document.getElementById('card-type');
    const cardImageElement = document.getElementById('card-image');

    const cardTypes = [
        { type: 'Visa', pattern: /^4/ },
        { type: 'MasterCard', pattern: /^5[1-5]/ },
        { type: 'amex', pattern: /^3[47]/ },
    ];

    const matchingCardType = cardTypes.find(card => card.pattern.test(cardNumber));

    if (matchingCardType) {
        cardTypeElement.innerHTML = `<i class="fa-brands fa-cc-${matchingCardType.type.toLowerCase()}"></i>`;
        showCardImage(matchingCardType.type);
    } else {
        cardTypeElement.textContent = '';
        hideCardImage();
    }
}

function showCardImage(cardType) {
    const cardImageElement = document.getElementById('card-image');

    cardImageElement.innerHTML = `<i class="fa-brands fa-cc-${cardType.toLowerCase()}"></i>`;
}

function hideCardImage() {
    const cardImageElement = document.getElementById('card-image');
    
    cardImageElement.innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function() {
    const decrementLinks = document.querySelectorAll('.decrement-link');

    decrementLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            decrementItem(productId);
        });
    });

    function decrementItem(productId) {
        fetch(`/decrement_item/${productId}/`, {
            method: 'GET', // vai 'POST', atkarībā no jūsu servera konfigurācijas
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Ja izmantojat CSRF aizsardzību
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atjaunināt lapas saturu, piemēram, span ar id="quantity"
                const quantityElement = document.getElementById('quantity');
                quantityElement.textContent = data.new_quantity;
            } else {
                console.error('Neizdevās samazināt!');
            }
        })
        .catch(error => {
            console.error('Kļūda veicot pieprasījumu:', error);
        });
    }

    // Palīgfunkcija CSRF žetona iegūšanai
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        return parts.length === 2 ? parts.pop().split(';').shift() : null;
    }
});

$(document).ready(function() {
    // Pievienojam notikumu klausītājus uz groza darbībām
    $('.action-link').click(function(event) {
        event.preventDefault(); // Pārtraucam noklusēto saites darbību

        var action = $(this).data('action'); // Noskaidrojam darbību (increment vai decrement)
        var productId = $(this).closest('.detail').find('#quantity').data('product-id'); // Iegūstam produkta ID

        if (action === 'increment') {
            // Izpildam pievienošanas darbību
            incrementQuantity(productId);
        } else if (action === 'decrement') {
            // Izpildam samazināšanas darbību
            decrementQuantity(productId);
        }
    });

    // Pievienojam notikumu klausītāju uz produktu noņemšanas darbību
    $('.product-close-btn').click(function(event) {
        event.preventDefault(); // Pārtraucam noklusēto saites darbību

        var productId = $(this).data('product-id');
        // Izpildam produktu noņemšanas darbību
        removeItemFromCart(productId);
    });
});

// Funkcija, kas palielina produkta daudzumu grozā
function incrementQuantity(productId) {
    // Veicam AJAX pieprasījumu, lai palielinātu produkta daudzumu grozā
    $.ajax({
        type: 'POST',
        url: '/cart/item_increment/' + productId + '/',
        success: function(response) {
            $('.product-card[data-product-id="' + productId + '"] #quantity').text(response.quantity);
            $('#total-price').text(response.total_amount);
            updateTotal();
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

// Funkcija, kas samazina produkta daudzumu grozā
function decrementQuantity(productId) {
    // Veicam AJAX pieprasījumu, lai samazinātu produkta daudzumu grozā
    $.ajax({
        type: 'POST',
        url: '/cart/item_decrement/' + productId + '/',
        success: function(response) {
            $('.product-card[data-product-id="' + productId + '"] #quantity').text(response.quantity);
            $('#total-price').text(response.total_amount);
            updateTotal();
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function removeItemFromCart(productId) {
    $.ajax({
        type: 'POST',
        url: '/cart/item_clear/' + productId + '/',
        success: function(response) {
            $('#total-price').text(response.total_amount);
            updateTotal();
            $('.product-card[data-product-id="' + productId + '"]').remove();
            if (response.cart_count === 0) {
                $('#cart-count').remove();
            } else {
                $('#cart-count').text(response.cart_count);
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
            // Atrodam CSRF sīkdatni pēc nosaukuma
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const particles = document.querySelector(".particles");

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement("span");
        const angle = Math.random() * 2 * Math.PI;
        const radius = Math.random() * 80 + 80;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        particle.style.setProperty("--x", x);
        particle.style.setProperty("--y", y);
        particle.style.animationDelay = `${Math.random() * 3}s`;

        particles.appendChild(particle);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    if (window.location.href.includes("/success/")) {
        document.querySelector(".order-confirmation").style.display = "block";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const viewOrderBtn = document.querySelector('.view-order');
    const continueShoppingBtn = document.querySelector('.continue-shopping');

    viewOrderBtn.addEventListener('click', function() {
        window.location.href = '/account';
    });

    continueShoppingBtn.addEventListener('click', function() {
        window.location.href = '/';
    });
});