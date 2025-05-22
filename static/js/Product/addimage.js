import $ from 'jquery';
import 'jquery-ui/ui/widget';
import 'jquery-ui/ui/widgets/mouse';
import 'jquery-ui/ui/widgets/draggable';
import 'jquery-ui/ui/widgets/resizable';
import 'jquery-ui-touch-punch';

function initDesignTools() {
    const Front = $('#front');
    const Back = $('#back');
    const rotate = $('#roatateicon');

    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    // Parāda/Slēpj front/back zonas atbilstoši
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
            hideHandles();
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
            const imageId = Date.now() + Math.random(); // unikāls ID

            reader.onload = function (event) {
                const selectedContainer = $(`#image-container-${currentSide}`);
                const selectedBoundary = document.getElementById(`boundary-${currentSide}`);

                if (!selectedBoundary || selectedContainer.length === 0) return;

                const boundaryRect = selectedBoundary.getBoundingClientRect();
                const containerOffset = selectedContainer[0].getBoundingClientRect();
                const relativeLeft = (boundaryRect.width / 2) - 75;
                const relativeTop = (boundaryRect.height / 2) - 75;

                // Mazais priekšskatījuma attēls
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

                // Lielais dizaina attēls
                const designImageHTML = `
                    <div class="uploaded-img-product element-image ${currentSide}" data-image-id="${imageId}"
                         style="z-index:2; position:absolute; background:transparent;
                         left:${boundaryRect.left - containerOffset.left + relativeLeft}px;
                         top:${boundaryRect.top - containerOffset.top + relativeTop}px;">
                        <img src="${event.target.result}" class="no-search editable-image resizable-image" draggable="true"
                             style="background:transparent; object-fit:contain; max-width:150px; height:auto;">
                    </div>
                `;
                selectedContainer.prepend(designImageHTML);

                const imgElement = $(`.uploaded-img-product[data-image-id="${imageId}"] .editable-image`);
                if (imgElement.length > 0) {
                    imgElement.attr('draggable', false);

                    imgElement.resizable({
                        handles: 'ne, se, sw, nw, n, e, s, w',
                        ghost: false,
                        containment: `#boundary-${currentSide}`,
                        maxWidth: selectedContainer.width(),
                        maxHeight: selectedContainer.height(),
                        start: (event, ui) => {
                            ui.element.data('startTop', ui.position.top);
                            ui.element.data('startLeft', ui.position.left);
                        },
                        resize: (event, ui) => {
                            ui.position.top = ui.element.data('startTop');
                            ui.position.left = ui.element.data('startLeft');
                        }
                    }).parent().draggable({
                        containment: `#boundary-${currentSide}`
                    });
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
            <div id="image-settings" class="settings-panel">
                <h3>${gettext("Picture settings")}</h3>
                <div class="input-group">
                    <div class="input-item">
                        <label for="z-index">${gettext("Layer order")}:</label>
                        <input type="number" id="z-index" value="${originalStyles.zIndex}">
                    </div>
                    <div class="input-item">
                        <label for="rotate">${gettext("Rotation")}:</label>
                        <input type="number" id="rotate" value="${originalStyles.rotate}">
                    </div>
                </div>
                <button id="apply-settings">${gettext("Customize")}</button>
                <button id="cancel-settings">${gettext("Cancel")}</button>
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
            $('#image-settings').hide();
            uploadWrapper.show();
        });
    });
}

document.addEventListener('DOMContentLoaded', initDesignTools);
