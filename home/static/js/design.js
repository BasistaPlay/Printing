// -----------Side-----------
document.addEventListener('DOMContentLoaded', function() {
    // Pārbaudam, vai lokālā krātuve jau satur vērtību
    let currentSide = localStorage.getItem('currentSide');
    
    // Ja lokālā krātuve ir tukša vai nesatur pareizu vērtību, iestatam noklusējuma vērtību uz "front"
    if (!currentSide || (currentSide !== 'front' && currentSide !== 'back')) {
        currentSide = 'front';
        localStorage.setItem('currentSide', currentSide);
    } else if (currentSide === 'back') {
        // Ja sākotnējā vērtība bija "back", tad to mainām uz "front"
        currentSide = 'front';
        localStorage.setItem('currentSide', currentSide);
    }

// -----------Color-----------
    const colorElements = document.querySelectorAll('.color-select');
    const colorContainer = document.querySelector('.color');

    colorElements.forEach(function(colorElement, index) {
        colorElement.addEventListener('click', function() {
            const selectedColor = colorElement.style.backgroundColor;

            colorContainer.style.backgroundColor = selectedColor;

            colorElements.forEach(function(element) {
                element.classList.remove('active-color');
            });
            colorElement.classList.add('active-color');
        });
    });

    // var numbers = document.getElementById('box');

    // for(i=0; i<20; i++){
    //     var span = document.createElement('span');
    //     span.textContent = i
    //     numbers.appendChild(span)
    // }

    // var num = numbers.getElementsByTagName('span')
    // var index = 0

    // $('#quanity-next').click(function() {
    //     num[index].style.display = 'none'
    //     index = (index + 1) % num.length
    //     num[index].style.display = 'initial'
    // })

    // $('#quanity-prev').click(function() {
    //     num[index].style.display = 'none'
    //     index = (index - 1 + num.length) % num.length
    //     num[index].style.display = 'initial'
    // })

    // -----------Image-----------
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
        handles: 'ne, se, sw, nw, middle-n, middle-w, middle-s, middle-e',
        ghost: false,
        border: false
    });

    resizableElement = $(this);

    previousImageWidth = resizableElement.width();
    $('.ui-wrapper').draggable();
});


$(document).on('click', '.remove-btn', function() {
    let imageIdToRemove = $(this).parent().data('image-id');
    
    $('[data-image-id="' + imageIdToRemove + '"]').remove();

    let listItemToRemove = $('.text-list-item').eq(imageIdToRemove);
    listItemToRemove.remove();
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
                    <div class='uploaded-img ${currentSide}' data-image-id='${imageId}'>
                        <img src='${event.target.result}' draggable='true'>
                        <button type='button' class='remove-btn'>
                            <i class='fas fa-times'></i>
                        </button>
                    </div>
                    `;
                    $('.upload-img').append(htmlList);

                    let htmlKrekls = `
                    <div class='uploaded-img element-image ${currentSide}' data-image-id='${imageId}'>
                        <img src='${event.target.result}' class='editable-image resizable-image' draggable='true'>
                    </div>
                `;
                    let selectedContainer;
                    if (currentSide === 'front') {
                        selectedContainer = $('#front');
                    } else {
                        selectedContainer = $('#back');
                    }
                    let parentContainer = $('<div class="parent-container" style="position: relative; width: 100%; height: 100%;"></div>');

                    selectedContainer.prepend(htmlKrekls);

                    $('.remove-btn').click(function() {
                        let imageIdToRemove = $(this).parent().data('image-id');
                        $('[data-image-id="' + imageIdToRemove + '"]').remove();
                    });

                    $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`).resizable({
                        handles: 'ne, se, sw, nw, middle-n, middle-w, middle-s, middle-e',
                        ghost: false,
                        border: false
                    });
    
                    $('.ui-wrapper').draggable();


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


    // -----------Text-----------


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
            textElement.innerHTML = `<span class="editable-text" style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value}; z-index: 6;">${text}</span>`;
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

            $('.editable-text').draggable();

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

});
