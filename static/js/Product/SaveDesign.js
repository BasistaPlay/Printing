function saveImage(side, callback) {
    var productDiv = document.querySelector('.product');
    var parentWidth = productDiv.offsetWidth;
    var parentHeight = productDiv.offsetHeight;

    var boundaries = document.querySelectorAll('.boundary');
    boundaries.forEach(boundary => boundary.style.display = 'none');

    productDiv.style.width = parentWidth + 'px';
    productDiv.style.height = parentHeight + 'px';

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');

    canvas.width = parentWidth;
    canvas.height = parentHeight;

    html2canvas(productDiv).then(function(renderedCanvas) {
        context.drawImage(renderedCanvas, 0, 0, parentWidth, parentHeight);

        var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        var data = imageData.data;

        var pixelCount = {};

        for (var i = 0; i < data.length; i += 4) {
            var r = data[i];
            var g = data[i + 1];
            var b = data[i + 2];
            var key = r + ',' + g + ',' + b;

            if (!pixelCount[key]) {
                pixelCount[key] = 0;
            }

            pixelCount[key]++;
        }

        var maxCount = 0;
        var backgroundColorKey;

        for (var key in pixelCount) {
            if (pixelCount[key] > maxCount) {
                maxCount = pixelCount[key];
                backgroundColorKey = key;
            }
        }

        var rgbValues = backgroundColorKey.split(',').map(function(value) {
            return parseInt(value);
        });

        for (var i = 0; i < data.length; i += 4) {
            var r = data[i];
            var g = data[i + 1];
            var b = data[i + 2];

            if (r === rgbValues[0] && g === rgbValues[1] && b === rgbValues[2]) {
                data[i + 3] = 0;
            }
        }

        var trimHeight = 15;
        context.clearRect(0, canvas.height - trimHeight, canvas.width, trimHeight);

        context.putImageData(imageData, 0, 0);

        var base64URL = canvas.toDataURL('image/png');

        callback(side, base64URL);

        boundaries.forEach(boundary => boundary.style.display = 'block');
    });
}



$('#buy-button').click(function() {
    var publishCheckbox = $('#publish-checkbox').is(":checked");
    var activeColor = $('.color-select.active-color').attr('data-color-name');
    var productSlug = $('#product-slug').val();
    var title = $('#title-input').val() || '';

    var errorHtml = '';

    if (!activeColor) {
        errorHtml += '<p>' + `${gettext("Please select a color")}` + '</p>';
    }

    if (publishCheckbox) {
        if (!title.trim()) {
            errorHtml += '<p>' + `${gettext("Title is required")}` + '</p>';
        }
    }

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

    document.getElementById('front').style.display = 'block';
    document.getElementById('back').style.display = 'none';

    saveImage('front', function(side, base64URLFront) {
        formData.append(side + '_image', base64URLFront);
        document.getElementById('front').style.display = 'none';
        document.getElementById('back').style.display = 'block';
        saveImage('back', function(side, base64URLBack) {
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