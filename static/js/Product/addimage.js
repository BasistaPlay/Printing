import $ from 'jquery';
import 'jquery-ui/ui/widget';
import 'jquery-ui/ui/widgets/mouse';
import 'jquery-ui/ui/widgets/draggable';
import 'jquery-ui/ui/widgets/resizable';
import 'jquery-ui-touch-punch';

window.gettext = window.gettext || function(s) { return s; };

function initDesignTools() {
    const Front = $('#front');
    const Back = $('#back');
    const rotate = $('#roatateicon');

    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    function updateSideVisibility() {
        if (currentSide === 'front') {
            $('#boundary-front').show();
            $('#boundary-back').hide();
        } else {
            $('#boundary-front').hide();
            $('#boundary-back').show();
        }
    }

    updateSideVisibility();

    if (rotate.length > 0) {
        rotate.on('click', function () {
            currentSide = (currentSide === 'front') ? 'back' : 'front';
            localStorage.setItem('currentSide', currentSide);
            updateSideVisibility();
        });
    }

    const uploadInput = $('#upload-input');
    const uploadArea = $('.upload-area');
    const uploadWrapper = $('.upload-wrapper');

    if (uploadArea.length > 0) {
        uploadArea.on('click', () => {
            uploadInput.trigger('click');
        }).on('drop', function (event) {
            event.preventDefault();
            handleFiles(event.originalEvent.dataTransfer.files);
        }).on('dragover', function (event) {
            event.preventDefault();
        });
    }

    if (uploadInput.length > 0) {
        uploadInput.on('change', event => {
            if (event.target.files.length > 0) {
                handleFiles(event.target.files);
            }
        });
    }

    let activeImage = null;

    function hideHandles() {
        $('.ui-resizable-handle').hide();
    }

    function showHandles(imageElement) {
        imageElement.find('.ui-resizable-handle').show();
    }

    $(document).on('mousedown touchstart', function (event) {
        const clickedImage = $(event.target).closest('.uploaded-img-product');
        if (clickedImage.length > 0) {
            showHandles(clickedImage);
            activeImage = clickedImage;
        } else {
            hideHandles();
            activeImage = null;
        }
    }).on('keydown', function (event) {
        if (event.key === 'Delete' && activeImage) {
            const imageId = activeImage.data('image-id');
            $(`[data-image-id="${imageId}"]`).remove();
            activeImage = null;
        }
    });

    function handleFiles(files) {
        if (!files || files.length === 0) return;

        for (let i = 0; i < files.length; i++) {
            const reader = new FileReader();
            const file = files[i];
            const imageId = Date.now() + Math.random();

            reader.onload = function (event) {
            const selectedContainer = $(`#image-container-${currentSide}`);
            const selectedBoundary = document.getElementById(`boundary-${currentSide}`);

            if (!selectedBoundary || selectedContainer.length === 0) return;

            const boundaryRect = selectedBoundary.getBoundingClientRect();
            const containerOffset = selectedContainer[0].getBoundingClientRect();
            const relativeLeft = (boundaryRect.width / 2) - 75;
            const relativeTop = (boundaryRect.height / 2) - 75;

            const previewHTML = `
                <div class="uploaded-img ${currentSide} relative group rounded-lg overflow-hidden shadow-md w-32 h-32 border border-gray-300" data-image-id="${imageId}">
                <img src="${event.target.result}" alt="uploaded"
                    class="w-full h-full object-contain bg-white no-search pointer-events-none" draggable="false" />
                <button type="button"
                        class="remove-btn absolute top-1 right-1 bg-white rounded-full p-1 shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
                        aria-label="Remove image">
                    <svg width="16" height="16" class="text-[var(--main-color)]">
                    <use xlink:href="/static/svg/sprite.svg#x-circle"></use>
                    </svg>
                </button>
                </div>
            `;
            $('.upload-img').append(previewHTML);

            const designImageHTML = `
                <div class="uploaded-img-product element-image ${currentSide}" data-image-id="${imageId}"
                    style="z-index:2; position:absolute; background:transparent;
                    left:${boundaryRect.left - containerOffset.left + relativeLeft}px;
                    top:${boundaryRect.top - containerOffset.top + relativeTop}px;">
                <img src="${event.target.result}" class="no-search editable-image resizable-image"
                    draggable="false"
                    style="background:transparent; object-fit:contain; max-width:150px; height:auto;">
                </div>
            `;
            selectedContainer.prepend(designImageHTML);

            const $imgWrapper = $(`.uploaded-img-product[data-image-id="${imageId}"]`);
            const $img = $imgWrapper.find('img');

            $img.on('load', function () {
                if ($img.width() === 0 || $img.height() === 0) {
                $img.css({
                    width: '150px',
                    height: 'auto'
                });
                }

                $img.resizable({
                handles: 'ne, se, sw, nw, n, e, s, w',
                containment: `#boundary-${currentSide}`,
                ghost: false,
                start: (event, ui) => {
                    ui.element.data('startTop', ui.position.top);
                    ui.element.data('startLeft', ui.position.left);
                },
                resize: (event, ui) => {
                    ui.position.top = ui.element.data('startTop');
                    ui.position.left = ui.element.data('startLeft');
                }
                });

                $imgWrapper.draggable({
                containment: `#boundary-${currentSide}`
                });

            });

            if ($img[0].complete) {
                $img.trigger('load');
            }

            $('.remove-btn').click(function () {
                const imageIdToRemove = $(this).parent().data('image-id');
                $(`[data-image-id="${imageIdToRemove}"]`).remove();
            });
            };

            reader.readAsDataURL(file);
        }
    }


    $(document).on('click', '.uploaded-img', function () {
        const imageId = $(this).data('image-id');
        const $imageContainer = $(`.uploaded-img-product[data-image-id="${imageId}"]`);
        const image = $imageContainer.find('img')[0];

        if (!image) return;

        const originalStyles = {
            zIndex: $imageContainer.css('z-index'),
            rotate: image.style.transform ? parseInt(image.style.transform.replace(/[^\d-]/g, '')) : 0,
        };

        uploadWrapper.hide();
        $('#image-settings').remove();

        const settingsPanel = `
        <!-- Overlay fons -->
        <div id="image-settings-overlay" class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-40"></div>

        <!-- Pašreizējais logs -->
        <div id="image-settings" class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white shadow-xl rounded-xl p-4 w-80 space-y-4 z-50 border border-gray-200">
            <h3 class="text-lg font-semibold text-[var(--main-color)]">${gettext("Picture settings")}</h3>

            <div class="space-y-2">
            <div class="flex flex-col">
                <label for="z-index" class="text-sm font-medium text-gray-600">${gettext("Layer order")}:</label>
                <input type="number" id="z-index" class="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring focus:ring-[var(--main-color)] focus:border-[var(--main-color)] transition">
            </div>

            <div class="flex flex-col">
                <label for="rotate" class="text-sm font-medium text-gray-600">${gettext("Rotation")}:</label>
                <input type="number" id="rotate" class="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring focus:ring-[var(--main-color)] focus:border-[var(--main-color)] transition">
            </div>
            </div>

            <div class="flex justify-end space-x-2 pt-2">
            <button id="apply-settings" class="px-3 py-1 rounded bg-[var(--main-color)] text-white hover:bg-opacity-90 transition">${gettext("Customize")}</button>
            <button id="cancel-settings" class="px-3 py-1 rounded border border-gray-300 text-gray-700 hover:bg-gray-100 transition">${gettext("Cancel")}</button>
            </div>
        </div>
        `;

        $('#upload').append(settingsPanel);

        $('#z-index').on('input', function () {
            $imageContainer.css('z-index', $(this).val());
        });

        $('#rotate').on('input', function () {
            image.style.transform = `rotate(${this.value}deg)`;
        });

        $('#apply-settings').on('click', function () {
            $('#image-settings').hide();
            uploadWrapper.show();
        });

        $('#cancel-settings').on('click', function () {
            $imageContainer.css('z-index', originalStyles.zIndex);
            image.style.transform = `rotate(${originalStyles.rotate}deg)`;
            $('#image-settings, #image-settings-overlay').remove();
            uploadWrapper.show();
        });
    });
}

document.addEventListener('DOMContentLoaded', initDesignTools);
