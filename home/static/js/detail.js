
// input
const input = document.querySelector(".order__quantity--input");
const minusBtn = document.querySelector(".minus");
const plusBtn = document.querySelector(".plus");

minusBtn.onclick = () => (input.value > 0) ?input.value-- :input.value;
plusBtn.onclick = () => input.value++;


// Add to cart & Remove from cart
const cartBtn = document.querySelector(".header__cart-icon");
const cart = document.querySelector(".cart");
const cartQuantityBubble = document.querySelector(".cart-icon--quantity");
const addToCartBtn = document.querySelector(".order__cart");
const cartContainer = document.querySelector(".cart-content");
const productElement = document.createElement("div");
const removeFromCartBtn = document.createElement("button");


productElement.classList.add("cart__product");
removeFromCartBtn.classList.add(".cart__product--delete");

let product = {
    name: "Fall Limited Edition Sneakers",
    price : 125,
    quantity: sessionStorage.getItem("quantity") || 0,
};


const updateCart = () => {
    cartContainer.classList.remove("empty");
    cartQuantityBubble.classList.remove("empty");
    cartQuantityBubble.innerText = product.quantity;

    let total = product.price * product.quantity;

    let htmlCode = 
        `<img class="cart__product--img" src="./images/image-product-1-thumbnail.jpg" alt="">

        <div class="cart__product--info">
            <p class="cart__info--title">${product.name}</p>
            <span class="cart__info--quantity">$${product.price} x ${product.quantity}</span>
            <b class="cart__info--price">$${total}.00 </b>
        </div>`;

    productElement.innerHTML = htmlCode;
    productElement.appendChild(removeFromCartBtn);
    cartContainer.appendChild(productElement);
}

const addToCart = () => {
    if (input.value <= 0 || input.value == undefined || null) {
            alert("error");
            return;
    }
    
    cart.classList.add("active");
    cartContainer.classList.remove("empty");
    
    product.quantity = parseInt(product.quantity) + parseInt(input.value);

    updateCart();
    sessionStorage.setItem("quantity", product.quantity);
};

const removeFromCart = () => {
    if (!cartContainer.classList.contains("empty")) {
        cartContainer.removeChild(productElement);
        cartContainer.classList.add("empty");
        cartQuantityBubble.innerText = "";
        product.quantity = 0;
        sessionStorage.setItem("quantity", product.quantity);
    }
};

addToCartBtn.onclick = () => addToCart();
removeFromCartBtn.onclick = () => removeFromCart();

function changeFocusImage(newImageUrl, focusValue) {
    document.getElementById('focus-image').src = newImageUrl;
    // Jūs varat veikt papildu darbības, pamatojoties uz focusValue, ja tas ir nepieciešams
}


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