import $ from 'jquery';
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#buy-now").addEventListener("click", function (event) {
        var activeColor = document.querySelector('.color-select.active-color')?.getAttribute('data-color-name');
        var publishCheckbox = document.querySelector("#publish-checkbox")?.checked;
        var titleInput = document.querySelector("#title-input")?.value.trim();
        var errorHtml = '';

        if (!activeColor) {
            errorHtml += '<p>' + `${gettext("Please select a color")}` + '</p>';
        }

        if (publishCheckbox && !titleInput) {
            errorHtml += '<p>' + `${gettext("Title is required")}` + '</p>';
        }

        if (errorHtml) {
            document.getElementById('error-messages').innerHTML = errorHtml;
            document.getElementById('error-messages').classList.add('show');

            setTimeout(function () {
                document.getElementById('error-messages').classList.remove('show');
            }, 10000);

            event.preventDefault();
            return;
        }

        openBuyNowPopup();
    });
});

function openBuyNowPopup() {
    let originalProduct = document.querySelector("#original-product");

    if (!originalProduct) {
        console.error("Kļūda: Nevar atrast 'original-product'!");
        return;
    }

    let clonedProduct = originalProduct.cloneNode(true);
    clonedProduct.classList.add("cloned-product");

    let hiddenInputs = clonedProduct.querySelectorAll("input[type='hidden']");
    hiddenInputs.forEach(input => input.remove());

    let title = document.createElement("h2");
    title.innerText = `${gettext("Your Personalized Design Preview")}`;
    title.classList.add("text-xl", "lg:text-4xl", "font-bold", "mb-6", "text-center", "text-color");

    let front = clonedProduct.querySelector("#front");
    let back = clonedProduct.querySelector("#back");
    let color = clonedProduct.querySelector(".color");

    if (front && back) {
        front.classList.remove("hidden");
        back.classList.remove("hidden");
        front.style.display = "block";
        back.style.display = "block";

        let boundaryFront = front.querySelector("#boundary-front");
        let boundaryBack = back.querySelector("#boundary-back");
        if (boundaryFront) boundaryFront.remove();
        if (boundaryBack) boundaryBack.remove();

        let imageContainer = document.createElement("div");
        imageContainer.classList.add("flex", "items-center", "justify-center", "gap-4", "w-full", "max-md:flex-col");

        [front, back].forEach(side => {
            side.classList.add("relative", "w-[480px]", "h-[464px]");

            let overlay = document.createElement("div");
            overlay.classList.add(
                "absolute", "top-0", "left-0", "w-full", "h-full",
                "bg-transparent", "z-10"
            );
            overlay.style.pointerEvents = "all";
            side.appendChild(overlay);
        });

        let frontImg1 = front.querySelector(".img-1");
        let frontImg2 = front.querySelector(".img-2");
        let backImg1 = back.querySelector(".img-1");
        let backImg2 = back.querySelector(".img-2");

        [frontImg1, frontImg2, backImg1, backImg2].forEach(img => {
            if (img) {
                img.classList.add("w-[480px]", "h-[464px]");
            }
        });

        if (color) {
            let frontColor = color.cloneNode(true);
            let backColor = color.cloneNode(true);
            frontColor.classList.add("absolute", "top-0", "left-0", "w-[480px]", "h-[464px]");
            backColor.classList.add("absolute", "top-0", "left-0", "w-[480px]", "h-[464px]");

            front.appendChild(frontColor);
            back.appendChild(backColor);
        }

        imageContainer.appendChild(front);
        imageContainer.appendChild(back);

        clonedProduct.innerHTML = "";
        clonedProduct.appendChild(imageContainer);
    }

    let overlay = document.createElement("div");
    overlay.classList.add("fixed", "inset-0", "bg-black", "bg-opacity-50", "flex", "items-center", "justify-center", "z-50", 'max-md:pt-24');

    let wrapper = document.createElement("div");
    wrapper.classList.add("relative", "flex", "flex-col", "items-center", "bg-second-color", "p-6", "rounded-lg", "shadow-2xl", "max-md:w-[95%]", "max-sm:w-[90%]", "max-h-[85vh]", "overflow-y-auto");

    let closeButton = document.createElement("button");
    closeButton.innerText = "✖";
    closeButton.classList.add("absolute", "top-2", "right-2", "text-gray-500", "hover:text-red-500", "text-xl");
    closeButton.addEventListener("click", function () {
        overlay.remove();
        document.body.classList.remove("overflow-hidden");
    });

    let buyButton = document.createElement("button");
    buyButton.innerText = `${gettext("Add to Cart")}`;
    buyButton.id = "buy-button";
    buyButton.classList.add("base-page-btn", "mt-4");

    wrapper.appendChild(closeButton);
    wrapper.appendChild(title);
    wrapper.appendChild(clonedProduct);
    wrapper.appendChild(buyButton);
    overlay.appendChild(wrapper);

    document.body.appendChild(overlay);
    document.body.classList.add("overflow-hidden");
}






function saveImageFromClone(element, side, callback) {
    let parentWidth = element.offsetWidth;
    let parentHeight = element.offsetHeight;

    let boundaries = element.querySelectorAll('.boundary');
    boundaries.forEach(boundary => boundary.style.display = 'none');

    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d');

    canvas.width = parentWidth;
    canvas.height = parentHeight;

    html2canvas(element).then(function (renderedCanvas) {
        context.drawImage(renderedCanvas, 0, 0, parentWidth, parentHeight);

        let imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        let data = imageData.data;

        let pixelCount = {};
        for (let i = 0; i < data.length; i += 4) {
            let r = data[i];
            let g = data[i + 1];
            let b = data[i + 2];
            let key = r + ',' + g + ',' + b;

            if (!pixelCount[key]) {
                pixelCount[key] = 0;
            }
            pixelCount[key]++;
        }

        let maxCount = 0;
        let backgroundColorKey;
        for (let key in pixelCount) {
            if (pixelCount[key] > maxCount) {
                maxCount = pixelCount[key];
                backgroundColorKey = key;
            }
        }

        let rgbValues = backgroundColorKey.split(',').map(value => parseInt(value));

        for (let i = 0; i < data.length; i += 4) {
            let r = data[i];
            let g = data[i + 1];
            let b = data[i + 2];

            if (r === rgbValues[0] && g === rgbValues[1] && b === rgbValues[2]) {
                data[i + 3] = 0;
            }
        }

        context.putImageData(imageData, 0, 0);
        let base64URL = canvas.toDataURL('image/png');

        callback(side, base64URL);
        boundaries.forEach(boundary => boundary.style.display = 'block');
    });
}


$(document).on('click', '#buy-button', function () {
    var publishCheckbox = $('#publish-checkbox').is(":checked");
    var activeColor = document.querySelector('.color-select.active-color')?.getAttribute('data-color-name');
    var productSlug = $('#product-slug').val();
    var title = $('#title-input').val() || '';

    var errorHtml = '';


    if (errorHtml) {
        document.getElementById('error-messages').innerHTML = errorHtml;
        document.getElementById('error-messages').classList.add('show');
        setTimeout(function() {
            document.getElementById('error-messages').classList.remove('show');
        }, 10000);
        return;
    }

    var texts = [];
    document.querySelectorAll('#Text #text-list .text-list-item').forEach(function(item) {
        var text = item.querySelector('span').textContent.trim();
        if (text !== '') {
            var fontSize = window.getComputedStyle(item.querySelector('span')).fontSize;
            var fontColor = window.getComputedStyle(item.querySelector('span')).color;
            var fontFamily = window.getComputedStyle(item.querySelector('span')).fontFamily;

            texts.push({
                'text': text,
                'font_size': fontSize,
                'text_color': fontColor,
                'font_family': fontFamily
            });
        }
    });

    var images = [];
    document.querySelectorAll('#save-img img').forEach(function(img) {
        var imageData = img.src;
        images.push(imageData);
    });

    var formData = new FormData();
    formData.append('publish_product', publishCheckbox);
    formData.append('product_color', activeColor);
    formData.append('product_slug', productSlug);
    formData.append('product_title', title);
    formData.append('images', JSON.stringify(images));
    formData.append('texts', JSON.stringify(texts));

    let clonedProduct = document.querySelector('.cloned-product');
    let front = clonedProduct ? clonedProduct.querySelector('#front') : null;
    let back = clonedProduct ? clonedProduct.querySelector('#back') : null;

    if (!front || !back) {
        console.error("Kļūda: Nevar atrast priekšpusi vai aizmuguri klonētajam produktam!");
        return;
    }
    saveImageFromClone(front, 'front', function(side, base64URLFront) {
        formData.append(side + '_image', base64URLFront);
        saveImageFromClone(back, 'back', function(side, base64URLBack) {
            formData.append(side + '_image', base64URLBack);

            var csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
            formData.append('csrfmiddlewaretoken', csrfToken);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/product/save_design/', true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.onload = function () {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    var design_id = response.designs_id;
                    AddToCart(design_id);
                }
            };
            xhr.onerror = function () {
            };
            xhr.send(formData);
        });
    });
});


function displaySuccessMessage(message) {
    $('#success-message').text(message);
    $('#success-message').fadeIn();

    setTimeout(function() {
        $('#success-message').fadeOut();
    }, 5000);
}