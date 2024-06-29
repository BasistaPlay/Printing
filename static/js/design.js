document.addEventListener('DOMContentLoaded', function() {
    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    const colorElements = document.querySelectorAll('.color-select');
    const colorContainer = document.querySelector('.color');

    colorElements.forEach(function(colorElement) {
        colorElement.addEventListener('click', function() {
            const selectedColor = colorElement.style.backgroundColor;
            colorContainer.style.backgroundColor = selectedColor;

            colorElements.forEach(function(element) {
                element.classList.remove('active-color');
            });
            colorElement.classList.add('active-color');
        });
    });

    const plus = document.querySelector(".plus"),
        minus = document.querySelector(".minus"),
        num = document.querySelector(".num");

    let a = 1;

    plus.addEventListener('click', () => {
        a++;
        a = (a < 10) ? '0' + a : a;
        num.innerText = a;
    });

    minus.addEventListener('click', () => {
        if (a > 1) {
            a--;
            a = (a < 10) ? '0' + a : a;
            num.innerText = a;
        }
    });

    var sizeOptions = document.querySelectorAll('.size-option');

    sizeOptions.forEach(function(option) {
        option.addEventListener('click', function() {
            sizeOptions.forEach(function(opt) {
                opt.classList.remove('active');
            });

            this.classList.add('active');
        });
    });

    var infoIcon = document.querySelector('.info-icon');
    var modal = document.getElementById('info-modal');
    var closeBtn = document.querySelector('.close');

    infoIcon.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    $('.upload-area').click(function() {
        $('#upload-input').trigger('click');
    });

    $('#upload-input').change(event => {
        if (event.target.files) {
            handleFiles(event.target.files);
        }
    });

    $('.upload-area').on('drop', function(event) {
        event.preventDefault();
        let files = event.originalEvent.dataTransfer.files;
        handleFiles(files);
    });

    $('.upload-area').on('dragover', function(event) {
        event.preventDefault();
    });

    let resizableElement = null;
    let previousImageWidth = 0;

    $(document).on('mousedown', '.editable-image', function(event) {
        if (resizableElement && !$(this).is(resizableElement)) {
            resizableElement.resizable("destroy");
        }

        $(this).resizable({
            containment: `#boundary-${currentSide}`,
            handles: 'ne, se, sw, nw',
            ghost: false,
            stop: function(event, ui) {
                let parent = ui.element.parent();
                let position = parent.position();
                let width = parent.width();
                let height = parent.height();
                parent.css({
                    top: position.top,
                    left: position.left,
                    width: width,
                    height: height
                });
            }
        });

        resizableElement = $(this);

        previousImageWidth = resizableElement.width();
        $('.ui-wrapper').draggable({
            containment: `#boundary-${currentSide}`,
            stop: function(event, ui) {
                let wrapper = ui.helper;
                wrapper.css({
                    top: ui.position.top,
                    left: ui.position.left,
                });
            }
        });
    });

    $(document).on('click', '.remove-btn', function() {
        let imageIdToRemove = $(this).parent().data('image-id');
        $('[data-image-id="' + imageIdToRemove + '"]').remove();
    });

    $(document).on('mousedown', function(event) {
        if (!$(event.target).is('.editable-image')) {
            let newImageWidth = resizableElement.width();

            if (Math.abs(newImageWidth - previousImageWidth) > 10) {
                resizableElement.resizable("destroy");
                resizableElement = null;
            }

            previousImageWidth = 0;
        }
    });

    function handleFiles(files) {
        if (files) {
            let filesAmount = files.length;

            for (let i = 0; i < filesAmount; i++) {
                let reader = new FileReader();
                reader.onload = function(event) {
                    let imageId = Date.now();

                    let htmlList = `
                    <div class='uploaded-img ${currentSide}' data-image-id='${imageId}' id='save-img'>
                        <img src='${event.target.result}' draggable='true' style='background: transparent;'>
                        <button type='button' class='remove-btn'>
                            <i class='fas fa-times'></i>
                        </button>
                    </div>
                    `;
                    $('.upload-img').append(htmlList);

                    let htmlKrekls = `
                    <div class='uploaded-img element-image ${currentSide}' data-image-id='${imageId}' style='z-index:2; top:100px; background: transparent;'>
                        <img src='${event.target.result}' class='editable-image resizable-image' draggable='true' style='background: transparent;'>
                    </div>
                `;
                    let selectedContainer;
                    if (currentSide === 'front') {
                        selectedContainer = $('#front');
                    } else {
                        selectedContainer = $('#back');
                    }
                    selectedContainer.prepend(htmlKrekls);

                    // // Center the image for 1 second and then remove the centered class
                    // setTimeout(function() {
                    //     $(`.uploaded-img[data-image-id='${imageId}']`).removeClass('centered');
                    // }, 1000);

                    $('.remove-btn').click(function() {
                        let imageIdToRemove = $(this).parent().data('image-id');
                        $('[data-image-id="' + imageIdToRemove + '"]').remove();
                    });

                    $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`).resizable({
                        containment: `#boundary-${currentSide}`,
                        handles: 'ne, se, sw, nw, n, e, s, w',
                        ghost: false,
                        stop: function(event, ui) {
                            let parent = ui.element.parent();
                            let position = parent.position();
                            let width = parent.width();
                            let height = parent.height();
                            parent.css({
                                top: position.top,
                                left: position.left,
                                width: width,
                                height: height
                            });
                        }
                    }).parent().draggable({
                        containment: `#boundary-${currentSide}`,
                        ghost: false,
                        stop: function(event, ui) {
                            let wrapper = ui.helper;
                            wrapper.css({
                                top: ui.position.top,
                                left: ui.position.left,
                            });
                        }
                    });
                };
                reader.readAsDataURL(files[i]);
            }

            $('.upload-img').css('padding', '20px');
        }
    }

    $('.remove-btn').click(function() {
        let imageIdToRemove = $(this).parent().data('image-id');
        $('[data-image-id="' + imageIdToRemove + '"]').remove();
    });

    const generalContent = document.getElementById('general');
    const uploadContent = document.getElementById('upload');
    const AiContent = document.getElementById('Ai-generator');
    const Text = document.getElementById('Text');
    const Back = document.getElementById('back');
    const Front = document.getElementById('front');

    const generalIcon = document.getElementById('generalIcon');
    const imageIcon = document.getElementById('imageIcon');
    const textIcon = document.getElementById('textIcon');
    const ai = document.getElementById('Ai-generatoricon');
    const rotate = document.getElementById('roatateicon');

    generalIcon.addEventListener('click', function() {
        showContent(generalContent);
        hideContent(uploadContent);
        hideContent(AiContent);
        hideContent(Text);
    });

    textIcon.addEventListener('click', function() {
        showContent(Text);
        hideContent(uploadContent);
        hideContent(AiContent);
        hideContent(generalContent);
    });

    imageIcon.addEventListener('click', function() {
        showContent(uploadContent);
        hideContent(generalContent);
        hideContent(AiContent);
        hideContent(Text);
    });

    ai.addEventListener('click', function() {
        showContent(AiContent);
        hideContent(generalContent);
        hideContent(uploadContent);
        hideContent(Text);
    });

    rotate.addEventListener('click', function() {
        if (currentSide === 'front') {
            showContent(Back);
            hideContent(Front);
            currentSide = 'back';
        } else {
            showContent(Front);
            hideContent(Back);
            currentSide = 'front';
        }

        localStorage.setItem('currentSide', currentSide);
    });

    function hideContent(element) {
        element.style.display = 'none';
    }

    function showContent(element) {
        element.style.display = 'block';
    }

    let editingIndex = -1;
    let isDragging = false;
    let draggedElement = null;

    document.getElementById('addTextButton').addEventListener('click', addText);

    function addText() {
        const textInput = document.getElementById('text-input');
        const textList = document.getElementById('text-list');
        const fontSize = document.getElementById('font-size').value + 'px';
        const editButton = document.getElementById('addTextButton');

        editButton.innerHTML = '<i class="fas fa-plus"></i> Add text';

        const text = textInput.value.trim();

        if (text !== '') {
            const currentSide = getCurrentSide();
            const textContainer = document.getElementById('text-container');
            const textElement = document.createElement('div');
            textElement.innerHTML = `<span class="editable-text centered" style="left:244px; top:-241px; font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value}; z-index: 6;">${text}</span>`;
            textElement.classList.add('centered');
            const listItem = document.createElement('li');
            listItem.className = 'text-list-item';
            textContainer.appendChild(textElement);
            listItem.innerHTML = `
                <span style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value};">${text}</span>
                <button class="edit-button" onclick="editTextInList(this)"><i class="fas fa-edit"></i></button>
                <button class="delete-button" onclick="deleteText(this)"><i class="fas fa-trash-alt"></i></button>
            `;

            textList.appendChild(listItem);

            textElement.setAttribute('draggable', 'true');
            textElement.setAttribute('class', 'text-a');

            $('.editable-text').draggable({
                containment: `#boundary-${currentSide}`,
                stop: function(event, ui) {
                    ui.helper.css('transform', 'translate(-50%, -50%)');
                }
            });

            if (currentSide === 'front') {
                $('#front #text-container').append(textElement);
            } else {
                $('#back #text-container').append(textElement);
            }

            textInput.value = '';
        } else {
            alert('Please enter text before adding to the list.');
        }
    }

    window.editTextInList = function(button) {
        const listItem = button.parentNode;
        const textSpan = listItem.querySelector('span');
        const textInput = document.getElementById('text-input');
        const textContainer = document.getElementById('text-container');
        const editButton = document.getElementById('addTextButton');

        if (editButton) {
            editButton.innerHTML = '<i class="fas fa-edit"></i> Edit text';
        } else {
            console.error("Element with ID 'addTextButton' not found!");
        }

        const previousTextContent = textSpan.textContent;
        const previousFontFamily = textSpan.style.fontFamily;
        const previousFontSize = textSpan.style.fontSize;
        const previousFontColor = textSpan.style.color;

        textSpan.textContent = textInput.value;
        textSpan.style.fontFamily = document.getElementById('font-select').value;
        textSpan.style.fontSize = document.getElementById('font-size').value + 'px';
        textSpan.style.color = document.getElementById('font-color').value;

        editingIndex = Array.from(listItem.parentNode.children).indexOf(listItem);

        const editedElement = textContainer.children[editingIndex].querySelector('span');
        editedElement.textContent = textInput.value;
        editedElement.style.fontFamily = textSpan.style.fontFamily;
        editedElement.style.fontSize = textSpan.style.fontSize;
        editedElement.style.color = textSpan.style.color;

        textInput.value = previousTextContent;
        document.getElementById('font-select').value = previousFontFamily;
        document.getElementById('font-size').value = parseInt(previousFontSize);
        document.getElementById('font-color').value = previousFontColor;
        hideEmptyTextItems();
    }

    function hideEmptyTextItems() {
        const textList = document.getElementById('text-list');
        const listItems = textList.querySelectorAll('.text-list-item');

        listItems.forEach(item => {
            const textSpan = item.querySelector('span');
            if (textSpan.textContent.trim() === '') {
                item.style.display = 'none';
            } else {
                item.style.display = '';
            }
        });
    }

    window.deleteText = function(button) {
        const listItem = button.parentNode;
        const textList = document.getElementById('text-list');
        const textContainer = document.getElementById('text-container');

        listItem.remove();
        textContainer.innerHTML = "";

        for (let i = 0; i < textList.children.length; i++) {
            const listItem = textList.children[i];
            const textSpan = listItem.querySelector('span');

            const textElement = document.createElement('div');
            textElement.innerHTML = `<span class="editable-text" style="font-size: ${textSpan.style.fontSize}; color: ${textSpan.style.color}; font-family: ${textSpan.style.fontFamily};">${textSpan.textContent}</span>`;
            textContainer.appendChild(textElement);
        }

        editingIndex = -1;
    }

    function getCurrentSide() {
        return currentSide;
    }

    var publishCheckbox = document.getElementById('publish-checkbox');
    var additionalInfo = document.getElementById('additional-info');

    publishCheckbox.addEventListener('change', function() {
        if (this.checked) {
            additionalInfo.style.display = 'block';
        } else {
            additionalInfo.style.display = 'none';
        }
    });

    function saveImage(side, callback) {
        var productDiv = document.querySelector('.product');
        var parentWidth = productDiv.offsetWidth;
        var parentHeight = productDiv.offsetHeight;

        // Hide boundaries before capturing the image
        var boundaries = document.querySelectorAll('.boundary');
        boundaries.forEach(boundary => boundary.style.display = 'none');

        productDiv.style.width = parentWidth + 'px';
        productDiv.style.height = parentHeight + 'px';

        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');

        canvas.width = parentWidth;
        canvas.height = parentHeight;

        html2canvas(productDiv).then(function (renderedCanvas) {
            context.drawImage(renderedCanvas, 0, 0, parentWidth, parentHeight);

            var base64URL = canvas.toDataURL('image/png');
            callback(side, base64URL);

            // Restore boundaries after capturing the image
            boundaries.forEach(boundary => boundary.style.display = 'block');
        });
    }

    $('#buy-button').click(function() {
        var publishCheckbox = $('#publish-checkbox').is(":checked");
        var numValue = $('.num').text();
        var activeSize = $('.size-option.active').attr('data-value');
        var activeColor = $('.color-select.active-color').attr('data-color-name');
        var productSlug = $('#product-slug').val();
        var title = $('#title-input').val();
        var description = $('#description-input').val();

        var errorHtml = '';

        if (!activeColor) {
            errorHtml += '<p>' + 'Please select a color' + '</p>';
        }

        if (!activeSize && $('.size-option').length > 0) {
            errorHtml += '<p>' + 'Please select a size' + '</p>';
        }

        if (publishCheckbox) {
            if (!title.trim()) {
                errorHtml += '<p>' +  'Title is required' + '</p>';
            }

            if (!description.trim()) {
                errorHtml += '<p>' + 'Description is required' + '</p>';
            }
        }
        if (errorHtml) {
            $('#error-messages').html(errorHtml).addClass('show');
            setTimeout(function() {
                $('#error-messages').removeClass('show');
            }, 10000);
            return;
        }

        var texts = [];
        $('#Text #text-list .text-list-item').each(function() {
            var text = $(this).find('span').text().trim();
            if (text !== '') {
                var fontSize = $(this).find('span').css('font-size');
                var fontColor = $(this).find('span').css('color');
                var fontFamily = $(this).find('span').css('font-family');

                texts.push({
                    'text': text,
                    'font_size': fontSize,
                    'text_color': fontColor,
                    'font_family': fontFamily
                });
            }
        });

        var images = [];
        $('#save-img img').each(function() {
            var imageData = $(this).attr('src');
            images.push(imageData);
        });

        var formData = new FormData();
        formData.append('publish_product', publishCheckbox);
        formData.append('num_value', numValue);
        formData.append('product_color', activeColor);
        formData.append('product_size', activeSize);
        formData.append('product_slug', productSlug);
        formData.append('product_title', title);
        formData.append('product_description', description);
        formData.append('images', JSON.stringify(images));
        formData.append('texts', JSON.stringify(texts));

        $('#front').css('display', 'block');
        $('#back').css('display', 'none');

        saveImage('front', function(side, base64URLFront) {
            formData.append(side + '_image', base64URLFront);
            $('#front').css('display', 'none');
            $('#back').css('display', 'block');
            saveImage('back', function(side, base64URLBack) {
                formData.append(side + '_image', base64URLBack);

                var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
                formData.append('csrfmiddlewaretoken', csrfToken);

                $.ajax({
                    type: 'POST',
                    url: '/save_order/',
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(response) {
                        var orderId = response.order_id;
                        AddToCart(orderId)
                        displaySuccessMessage('Your order has been successfully saved!');
                    },
                    error: function(xhr, status, error) {
                        console.error(error);
                    }
                });
            });
        });
    });

    function AddToCart(order_id) {
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
                $(document).ready(function() {
                    var cartCountElement = $('#cart-count');
                    if (cartCountElement.length === 0) {
                        var newCartCountElement = $('<span id="cart-count"></span>');
                        newCartCountElement.text(response.cart_count);
                        $('#cart').append(newCartCountElement);
                    } else {
                        cartCountElement.text(response.cart_count);
                    }
                });
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

    function displaySuccessMessage(message) {
        $('#success-message').text(message);
        $('#success-message').fadeIn();

        setTimeout(function() {
            $('#success-message').fadeOut();
        }, 5000);
    }

    const token = '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';
    const InputTxt = document.getElementById('textInput-Ai');
    const image = document.getElementById('image');
    const button = document.getElementById('generateButton');
    const loader = document.getElementById('loader');

    async function query() {
        loader.style.display = 'block';

        const response = await fetch(
            "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image",
            {
                headers: { Authorization: `Bearer ${token}` },
                method: "POST",
                body: JSON.stringify({'inputs': InputTxt.value}),
            }
        );
        const result = await response.blob();

        loader.style.display = 'none';

        image.onload = function() {
            document.getElementById('sendToImageBtn').style.display = 'flex';
        };

        image.src = URL.createObjectURL(result);
    }

    button.addEventListener('click', async function(){
        document.getElementById('sendToImageBtn').style.display = 'none';
        query();
    });

    document.getElementById('sendToImageBtn').addEventListener('click', function() {
        const imageContainer = document.getElementById('image');
        const uploadImgContainer = document.querySelector('.upload-img');
        const imageId = Date.now();

        let selectedContainer;
        const frontContainer = document.getElementById('front');
        const backContainer = document.getElementById('back');

        if (frontContainer.style.display === 'block') {
            selectedContainer = frontContainer;
        } else {
            selectedContainer = backContainer;
        }

        if (selectedContainer) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = imageContainer.width;
            canvas.height = imageContainer.height;
            ctx.drawImage(imageContainer, 0, 0, canvas.width, canvas.height);
            const base64data = canvas.toDataURL();

            const sideId = selectedContainer.id;

            const newImg = document.createElement('img');
            newImg.className = 'uploaded-img element-image resizable-image centered';
            newImg.src = base64data;

            const htmlImage = `
                <div class='uploaded-img element-image ${sideId} centered ui-wrapper' style='z-index:2; top:100px; background: transparent;' data-image-id='${imageId}'>
                    <img src='${base64data}' class='editable-image resizable-image' draggable='true'>
                </div>
            `;

            selectedContainer.insertAdjacentHTML('afterbegin', htmlImage);

            // // Center the image for 1 second and then remove the centered class
            // setTimeout(function() {
            //     $(`.uploaded-img[data-image-id='${imageId}']`).removeClass('centered');
            // }, 1000);

            let $resizableImage = $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`);
            $resizableImage.resizable({
                containment: `#boundary-${sideId}`,
                handles: 'ne, se, sw, nw, n, e, s, w',
                ghost: false,
                stop: function(event, ui) {
                    let parent = ui.element.parent();
                    let position = parent.position();
                    let width = parent.width();
                    let height = parent.height();
                    parent.css({
                        top: position.top,
                        left: position.left,
                        width: width,
                        height: height
                    });
                }
            }).parent().draggable({
                containment: `#boundary-${sideId}`,
                ghost: false,
                stop: function(event, ui) {
                    let wrapper = ui.helper;
                    wrapper.css({
                        top: ui.position.top,
                        left: ui.position.left,
                    });
                }
            });
        } else {
            const errorMessage = document.getElementById('error-messages');
            errorMessage.innerText = 'Nevarēja noteikt aktīvo pusi. Lūdzu, izvēlieties aktīvo pusi, kurai pievienot attēlu.';
            errorMessage.style.display = 'block';
        }

        const canvas2 = document.createElement('canvas');
        const ctx2 = canvas2.getContext('2d');
        canvas2.width = imageContainer.width;
        canvas2.height = imageContainer.height;
        ctx2.drawImage(imageContainer, 0, 0, canvas2.width, canvas2.height);
        const base64data2 = canvas2.toDataURL();

        const newImg2 = document.createElement('img');
        newImg2.className = 'uploaded-img front';
        newImg2.src = base64data2;

        const newDiv2 = document.createElement('div');
        newDiv2.className = 'uploaded-image-container';
        newDiv2.id = 'save-img';
        newDiv2.setAttribute('data-image-id', imageId)

        const removeBtn2 = document.createElement('button');
        removeBtn2.type = 'button';
        removeBtn2.className = 'remove-btn';
        removeBtn2.innerHTML = '<i class="fas fa-times" aria-hidden="true"></i>';
        removeBtn2.addEventListener('click', function() {
            let imageIdToRemove = $(this).parent().data('image-id');
            $(`[data-image-id="${imageIdToRemove}"]`).remove();

            let listItemToRemove = $('.text-list-item').eq(imageIdToRemove);
            listItemToRemove.remove();
        });
        newDiv2.appendChild(newImg2);
        newDiv2.appendChild(removeBtn2);

        uploadImgContainer.appendChild(newDiv2);
    });
});
