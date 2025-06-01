import $ from 'jquery';
import 'jquery-ui/ui/widget';
import 'jquery-ui/ui/widgets/mouse';
import 'jquery-ui/ui/widgets/draggable';
import 'jquery-ui/ui/widgets/resizable';
import 'jquery-ui-touch-punch';
let currentSide = localStorage.getItem('currentSide') || 'front';
localStorage.setItem('currentSide', currentSide);

let editingIndex = -1;
let isDragging = false;
let draggedElement = null;

document.addEventListener('DOMContentLoaded', () => {
    const addTextButton = document.getElementById('addTextButton');
        if (addTextButton) {
        addTextButton.addEventListener('click', addText);
        }

    function addText() {
        const textInput = document.getElementById('text-input');
        const textList = document.getElementById('text-list');
        const fontSize = document.getElementById('font-size').value + 'px';
        const textColor = document.getElementById('font-color').value;
        const editButton = document.getElementById('addTextButton');
        const fontFamily = document.getElementById('font-select').value;

        editButton.innerHTML = '<i class="fas fa-plus"></i> Add text';

        const text = textInput.value.trim();
        if (text === '') {
            alert('Please enter text before adding to the list.');
            return;
        }

        const currentSide = getCurrentSide();
        const $container = $(`#text-container[data-side="${currentSide}"]`);

        const textElement = document.createElement('div');
        textElement.className = 'draggable-text absolute block max-w-[90%] w-auto';
        textElement.style.position = 'absolute';
        textElement.innerHTML = `
            <span class="editable-text break-words whitespace-normal"
                style="color: ${textColor}; font-size: ${fontSize}; font-family: ${fontFamily};">
                ${text}
            </span>`;

        $container.append(textElement);

        requestAnimationFrame(() => {
            const containerWidth = $container.width();
            const containerHeight = $container.height();

            const textSpan = textElement.querySelector('.editable-text');
            const textWidth = textSpan.offsetWidth;
            const textHeight = textSpan.offsetHeight;

            const centerX = (containerWidth - textWidth) / 2;
            const centerY = (containerHeight - textHeight) / 2;

            textSpan.style.maxWidth = `${containerWidth * 0.9}px`;
            textElement.style.left = `${centerX}px`;
            textElement.style.top = `${centerY}px`;
            textElement.style.width = `${textWidth}px`;
            textElement.style.height = `${textHeight}px`;

            addResizableAndDraggable(textElement, currentSide, fontSize);
        });

        const listItem = document.createElement('li');
        listItem.className = 'text-list-item flex items-center justify-between gap-2 bg-[var(--input-color)] px-3 py-2 rounded-lg shadow-sm mb-2';
        listItem.innerHTML = `
            <span class="text-[${textColor}] text-sm font-medium" style="font-size: ${fontSize};">
                ${text}
            </span>

            <div class="flex gap-2">
                <button class="edit-button p-1 rounded-md bg-[var(--main-color)] hover:bg-opacity-80 transition" onclick="editTextInList(this)">
                <svg width="20" height="20" class="fill-white">
                    <use xlink:href="/static/svg/sprite.svg#edit"></use>
                </svg>
                </button>

                <button class="delete-button p-1 rounded-md bg-red-500 hover:bg-red-600 transition" onclick="deleteText(this)">
                <svg width="20" height="20" class="fill-white">
                    <use xlink:href="/static/svg/sprite.svg#trash"></use>
                </svg>
                </button>
            </div>
        `;
        textList.appendChild(listItem);

        textInput.value = '';

        textElement.addEventListener('dblclick', function() {
            const textSpan = this.querySelector('.editable-text');
            textSpan.setAttribute('contenteditable', 'true');
            textSpan.focus();

            textSpan.addEventListener('blur', function() {
                textSpan.removeAttribute('contenteditable');
                const index = $(this).closest('.draggable-text').index();
                const listItem = document.getElementById('text-list').children[index];
                const listTextSpan = listItem.querySelector('span');
                listTextSpan.textContent = textSpan.textContent;
            }, { once: true });
        });
    }



    function addResizableAndDraggable(element, currentSide, fontSize) {
        const $element = $(element);
        let $container = $(`#text-container[data-side="${currentSide}"]`);


        function updateContainerSize() {
            let containerWidth = $container.width();
            let containerHeight = $container.height();
            return {
                maxWidth: containerWidth,
                maxHeight: containerHeight,
            };
        }

        let { maxWidth, maxHeight } = updateContainerSize();

        $(window).on('resize', function() {
            ({ maxWidth, maxHeight } = updateContainerSize());
        });

        $element.draggable({
            containment: `#boundary-${currentSide}`,
            scroll: false,
            stop: function(event, ui) {
                $(this).css({
                    left: ui.position.left + 'px',
                    top: ui.position.top + 'px'
                });
            }
        });
    }

    window.editTextInList = function(button) {
        const listItem = button.closest('li'); // Precīzāk nekā parentNode
        const textSpan = listItem.querySelector('span');
        const textInput = document.getElementById('text-input');
        const fontSelect = document.getElementById('font-select');
        const fontSizeInput = document.getElementById('font-size');
        const fontColorInput = document.getElementById('font-color');

        const currentSide = getCurrentSide();
        const $container = $(`#text-container[data-side="${currentSide}"]`);

        // Atrodi index
        const index = Array.from(listItem.parentNode.children).indexOf(listItem);
        const textElement = $container.children().eq(index).find('.editable-text')[0];

        // Aizpildi input laukus no boundary teksta
        textInput.value = textElement.textContent;
        fontSelect.value = textElement.style.fontFamily || '';
        fontSizeInput.value = parseInt(textElement.style.fontSize) || '';
        fontColorInput.value = textElement.style.color || '#000000';

        // Atjaunini “Add text” pogas tekstu
        const editButton = document.getElementById('addTextButton');
        editButton.innerHTML = '<i class="fas fa-edit"></i> Save changes';

        // Kad lietotājs spiež “Save”, atjaunina datus
        editButton.onclick = function() {
            const newText = textInput.value.trim();
            if (newText === '') {
                alert('Please enter some text!');
                return;
            }

            const newFontFamily = fontSelect.value;
            const newFontSize = fontSizeInput.value + 'px';
            const newColor = fontColorInput.value;

            // Atjaunina boundary tekstu
            textElement.textContent = newText;
            textElement.style.fontFamily = newFontFamily;
            textElement.style.fontSize = newFontSize;
            textElement.style.color = newColor;

            // Atjaunina sarakstā
            textSpan.textContent = newText;
            textSpan.style.fontFamily = newFontFamily;
            textSpan.style.fontSize = newFontSize;
            textSpan.style.color = newColor;

            // Atjauno pogu uz “Add text”
            editButton.innerHTML = '<i class="fas fa-plus"></i> Add text';
            editButton.onclick = addText;
        };
    };


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
        const listItem = button.closest('li');
        const textList = document.getElementById('text-list');

        const indexToDelete = Array.from(textList.children).indexOf(listItem);

        // Noņem no saraksta
        listItem.remove();

        // Noņem no text-container!
        const currentSide = getCurrentSide();
        const $container = $(`#text-container[data-side="${currentSide}"]`);
        $container.children().eq(indexToDelete).remove();

        editingIndex = -1;
    };



    function getCurrentSide() {
        return localStorage.getItem('currentSide') || 'front';
    }
});