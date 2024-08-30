let currentSide = localStorage.getItem('currentSide') || 'front';
localStorage.setItem('currentSide', currentSide);

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

        if (!textContainer) {
            console.error(`Text container not found for side: ${currentSide}`);
            return;
        }

        const textElement = document.createElement('div');
        textElement.className = 'draggable-text ui-draggable ui-draggable-handle ui-resizable';
        textElement.style.position = 'relative';
        textElement.style.left = '0';
        textElement.style.top = '0';
        textElement.innerHTML = `<span class="editable-text">${text}</span>`;
        textContainer.appendChild(textElement);

        requestAnimationFrame(() => {
            const containerWidth = textContainer.offsetWidth;
            const containerHeight = textContainer.offsetHeight;

            const textSpan = textElement.querySelector('.editable-text');
            textSpan.style.fontSize = fontSize;

            const textWidth = textSpan.offsetWidth;
            textElement.style.width = `${textWidth}px`;

            const elementWidth = textElement.offsetWidth;
            const elementHeight = textElement.offsetHeight;

            const centerX = (containerWidth - elementWidth) / 2;
            const centerY = (containerHeight - elementHeight) / 2;

            textElement.style.left = `${centerX}px`;
            textElement.style.top = `${centerY}px`;

            addResizableAndDraggable(textElement, currentSide, fontSize);
        });

        const listItem = document.createElement('li');
        listItem.className = 'text-list-item';
        listItem.innerHTML = `
            <span style="font-size: ${fontSize};">${text}</span>
            <button class="edit-button" onclick="editTextInList(this)">
                <svg width="20" height="20" style="fill: white">
                    <use xlink:href="/static/svg/sprite.svg#edit"></use>
                </svg>
            </button>

            <button class="delete-button" onclick="deleteText(this)">
                <svg width="20" height="20" style="fill: white">
                    <use xlink:href="/static/svg/sprite.svg#trash"></use>
                </svg>
            </button>
        `;

        textList.appendChild(listItem);

        textInput.value = '';
    } else {
        alert('Please enter text before adding to the list.');
    }
}
function addResizableAndDraggable(element, currentSide, fontSize) {
    const $element = $(element);
    let currentWidth, currentHeight;

    $element.draggable({
        containment: `#boundary-${currentSide}`,
        start: function(event, ui) {
            $(this).data('startLeft', ui.position.left);
            $(this).data('startTop', ui.position.top);
        },
        drag: function(event, ui) {
            ui.position.left = Math.round(ui.position.left);
            ui.position.top = Math.round(ui.position.top);
            $(this).css({
                left: ui.position.left,
                top: ui.position.top,
            });
        },
        stop: function(event, ui) {
            $(this).css({
                left: ui.position.left,
                top: ui.position.top,
            });
        }
    })
    $element.children('.editable-text').css({
        fontSize: fontSize,
    });
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