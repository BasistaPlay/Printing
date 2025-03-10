$(document).ready(function () {
    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    function showContent(element) {
        element.style.display = 'block';
    }

    function hideContent(element) {
        element.style.display = 'none';
    }

    const Back = $('#back');
    const Front = $('#front');
    const rotate = $('#roatateicon');

    rotate.on('click', function () {
        if (currentSide === 'front') {
            showContent(Back[0]);
            hideContent(Front[0]);
            currentSide = 'back';
        } else {
            showContent(Front[0]);
            hideContent(Back[0]);
            currentSide = 'front';
        }
        localStorage.setItem('currentSide', currentSide);
    });

    $('.upload-area').on('click', function () {
        $('#upload-input').trigger('click');
    }).on('drop', function (event) {
        event.preventDefault();
        handleFiles(event.originalEvent.dataTransfer.files);
    }).on('dragover', function (event) {
        event.preventDefault();
    });

    $('#upload-input').change(event => {
        if (event.target.files.length > 0) {
            handleFiles(event.target.files);
        }
    });

    let activeImage = null;

    function hideHandles() {
        $('.ui-resizable-handle').hide();
    }

    function showHandles(imageElement) {
        imageElement.find('.ui-resizable-handle').show();
    }

    $(document).on('mousedown touchstart', function (event) {
        let clickedImage = $(event.target).closest('.uploaded-img-product');
        if (clickedImage.length) {
            hideHandles();
            showHandles(clickedImage);
            activeImage = clickedImage;
        } else {
            hideHandles();
            activeImage = null;
        }
    }).on('keydown', function (event) {
        if (event.key === 'Delete' && activeImage) {
            let imageId = activeImage.data('image-id');
            $('[data-image-id="' + imageId + '"]').remove();
            activeImage = null;
        }
    });

    function handleFiles(files) {
        if (!files || files.length === 0) return;
        let filesAmount = files.length;

        for (let i = 0; i < filesAmount; i++) {
            let reader = new FileReader();
            let file = files[i];

            reader.onload = function (event) {
                let imageId = Date.now();
                let selectedContainer = currentSide === 'front' ? $('#front') : $('#back');

                let htmlList = `
                <div class='uploaded-img ${currentSide}' data-image-id='${imageId}' id='save-img'>
                    <img src='${event.target.result}' draggable='true' style='background: transparent; object-fit: contain;'>
                    <button type='button' class='remove-btn'>
                        <svg width="20" height="20" style="color: var(--main-color);">
                            <use xlink:href="/static/svg/sprite.svg#x-circle"></use>
                        </svg>
                    </button>
                </div>
                `;
                $('.upload-img').append(htmlList);

                let htmlKrekls = `
                <div class='uploaded-img-product element-image ${currentSide}' data-image-id='${imageId}' style='z-index:2; top:100px; background: transparent;'>
                    <img src='${event.target.result}' class='editable-image resizable-image' draggable='true' style='background: transparent; object-fit: contain;'>
                </div>`;
                selectedContainer.prepend(htmlKrekls);

                let imgElement = $(`.uploaded-img-product[data-image-id='${imageId}'] .editable-image`);
                imgElement.attr('draggable', false);

                $('.remove-btn').click(function () {
                    let imageIdToRemove = $(this).parent().data('image-id');
                    $('[data-image-id="' + imageIdToRemove + '"]').remove();
                });

                imgElement.resizable({
                    handles: 'ne, se, sw, nw, n, e, s, w',
                    ghost: false,
                    containment: `#boundary-${currentSide}`,
                    maxWidth: selectedContainer.width(),
                    maxHeight: selectedContainer.height(),
                    start: function (event, ui) {
                        ui.element.data('startTop', ui.position.top);
                        ui.element.data('startLeft', ui.position.left);
                    },
                    resize: function (event, ui) {
                        ui.position.top = ui.element.data('startTop');
                        ui.position.left = ui.element.data('startLeft');
                    }
                }).parent().draggable({ containment: `#boundary-${currentSide}` });
            };
            reader.readAsDataURL(file);
        }
    }


    $(document).on('click', '.uploaded-img', function () {
        let imageId = $(this).data('image-id');
        let $imageContainer = $('.uploaded-img-product[data-image-id="' + imageId + '"]');
        let image = $imageContainer.find('img')[0];

        let originalStyles = {
            zIndex: $imageContainer.css('z-index'),
            rotate: image.style.transform ? parseInt(image.style.transform.replace('rotate(', '').replace('deg)', '')) : 0,
        };

        $('.upload-wrapper').hide();
        $('#image-settings').remove();

        let settingsPanel = `
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
            </div>`;
        $('#upload').append(settingsPanel);

        $('#z-index').on('input', function () {
            $imageContainer.css('z-index', $(this).val());
        });

        $('#rotate').on('input', function () {
            image.style.transform = `rotate(${$(this).val()}deg)`;
        });

        $('#apply-settings').on('click', function () {
            $('#image-settings').hide();
            $('.upload-wrapper').show();
        });

        $('#cancel-settings').on('click', function () {
            $imageContainer.css('z-index', originalStyles.zIndex);
            image.style.transform = `rotate(${originalStyles.rotate}deg)`;
            $('#image-settings').hide();
            $('.upload-wrapper').show();
        });
    });
});
