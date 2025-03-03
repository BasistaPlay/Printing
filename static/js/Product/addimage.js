$(document).ready(function () {
    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    function showContent(element) {
        element.style.display = 'block';
    }

    function hideContent(element) {
        element.style.display = 'none';
    }

    const Back = document.getElementById('back');
    const Front = document.getElementById('front');

    const rotate = document.getElementById('roatateicon');
    rotate.addEventListener('click', function () {
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

    $('.upload-area').click(function () {
        $('#upload-input').trigger('click');
    });

    $('#upload-input').change(event => {
        if (event.target.files && event.target.files.length > 0) {
            handleFiles(event.target.files);
        }
    });

    $('.upload-area').on('drop', function (event) {
        event.preventDefault();
        let files = event.originalEvent.dataTransfer.files;
        handleFiles(files);
    });

    $('.upload-area').on('dragover', function (event) {
        event.preventDefault();
    });

    let resizableElement = null;
    let previousImageWidth = 0;
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
    });

    $(document).on('keydown', function (event) {
        if (event.key === 'Delete' && activeImage) {
            let imageIdToRemove = activeImage.data('image-id');
            $('[data-image-id="' + imageIdToRemove + '"]').remove();
            activeImage.remove();
            activeImage = null;
        }
    });

    if (resizableElement && !$(this).is(resizableElement)) {
        resizableElement.resizable("destroy");
    }

    $(this).resizable({
        handles: 'ne, se, sw, nw',
        ghost: false,
        stop: function (event, ui) {
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
        stop: function (event, ui) {
            let wrapper = ui.helper;
            wrapper.css({
                top: ui.position.top,
                left: ui.position.left,
            });
        }
    });

    $(document).on('mousedown touchstart', function (event) {
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
                reader.onload = function (event) {
                    let imageId = Date.now();

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
                    </div>
                `;
                    let selectedContainer;
                    if (currentSide === 'front') {
                        selectedContainer = $('#front');
                    } else {
                        selectedContainer = $('#back');
                    }
                    selectedContainer.prepend(htmlKrekls);

                    $('.remove-btn').click(function () {
                        let imageIdToRemove = $(this).parent().data('image-id');
                        $('[data-image-id="' + imageIdToRemove + '"]').remove();
                    });

                    $(`.uploaded-img-product[data-image-id='${imageId}'] .editable-image`).resizable({
                        handles: 'ne, se, sw, nw, n, e, s, w',
                        ghost: false,
                        containment: `#boundary-${currentSide}`,
                        maxWidth: selectedContainer.width(),
                        maxHeight: selectedContainer.height(),
                        resize: function (event, ui) {
                            ui.element.css({
                                position: 'absolute',
                                top: ui.originalPosition.top,
                                left: ui.originalPosition.left
                            });
                        },
                        stop: function (event, ui) {
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
                        stop: function (event, ui) {
                            let wrapper = ui.helper;
                            wrapper.css({
                                top: ui.position.top,
                                left: ui.position.left
                            });
                        }
                    });
                };

                reader.readAsDataURL(files[i]);
            }
            $('.upload-img').css('padding', '20px');
        }
        $(document).ready(function () {
            let currentSide = localStorage.getItem('currentSide') || 'front';
            localStorage.setItem('currentSide', currentSide);

            function showContent(element) {
                element.style.display = 'block';
            }

            function hideContent(element) {
                element.style.display = 'none';
            }

            const Back = document.getElementById('back');
            const Front = document.getElementById('front');

            const rotate = document.getElementById('roatateicon');
            rotate.addEventListener('click', function () {
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

            $('.upload-area').click(function () {
                $('#upload-input').trigger('click');
            });

            $('#upload-input').change(event => {
                if (event.target.files && event.target.files.length > 0) {
                    handleFiles(event.target.files);
                }
            });

            $('.upload-area').on('drop', function (event) {
                event.preventDefault();
                let files = event.originalEvent.dataTransfer.files;
                handleFiles(files);
            });

            $('.upload-area').on('dragover', function (event) {
                event.preventDefault();
            });

            function handleFiles(files) {
                if (files) {
                    let filesAmount = files.length;

                    for (let i = 0; i < filesAmount; i++) {
                        let reader = new FileReader();
                        reader.onload = function (event) {
                            let imageId = Date.now();

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
                            </div>
                        `;
                            let selectedContainer;
                            if (currentSide === 'front') {
                                selectedContainer = $('#front');
                            } else {
                                selectedContainer = $('#back');
                            }
                            selectedContainer.prepend(htmlKrekls);

                            $('.remove-btn').click(function () {
                                let imageIdToRemove = $(this).parent().data('image-id');
                                $('[data-image-id="' + imageIdToRemove + '"]').remove();
                            });

                            $(`.uploaded-img-product[data-image-id='${imageId}'] .editable-image`).resizable({
                                handles: 'ne, se, sw, nw, n, e, s, w',
                                ghost: false,
                                containment: `#boundary-${currentSide}`,
                                maxWidth: selectedContainer.width(),
                                maxHeight: selectedContainer.height(),
                                resize: function (event, ui) {
                                    ui.element.css({
                                        position: 'absolute',
                                        top: ui.originalPosition.top,
                                        left: ui.originalPosition.left
                                    });
                                },
                                stop: function (event, ui) {
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
                                stop: function (event, ui) {
                                    let wrapper = ui.helper;
                                    wrapper.css({
                                        top: ui.position.top,
                                        left: ui.position.left
                                    });
                                }
                            });
                        };

                        reader.readAsDataURL(files[i]);
                    }
                    $('.upload-img').css('padding', '20px');
                }
            }

            $(document).on('click', '.uploaded-img', function() {
                let imageId = $(this).data('image-id');
                let $imageContainer = $('.uploaded-img-product[data-image-id="' + imageId + '"]');
                let image = $imageContainer.find('img')[0];

                let originalStyles = {
                    zIndex: image.style.zIndex || '1',
                    rotate: image.style.transform ? parseInt(image.style.transform.replace('rotate(', '').replace('deg)', '')) : 0,
                };

                $('.upload-wrapper').hide();
                $('#image-settings').show();


                if ($('#image-settings').length === 0) {
                    let settingsPanel = `
                        <div id="image-settings" class="settings-panel">
                            <h3>${gettext("Attēla iestatījumi")}</h3>
                            <div class="input-group">
                                <div class="input-item">
                                    <label for="z-index">${gettext("Slāņa kārtība")}:</label>
                                    <input type="number" id="z-index">
                                </div>
                                <div class="input-item">
                                    <label for="rotate">${gettext("Rotācija")}:</label>
                                    <input type="number" id="rotate">
                                </div>
                            </div>
                            <button id="apply-settings">${gettext("Pielāgot")}</button>
                            <button id="cancel-settings">${gettext("Atcelt")}</button>
                        </div>
                    `;
                    $('#upload').append(settingsPanel);
                }

                $('#z-index').val(image.style.zIndex || $imageContainer.css('z-index') || 1);
                $('#rotate').val(image.style.transform ?
                    parseInt(image.style.transform.replace('rotate(', '').replace('deg)', '')) : 0);

                $('#z-index').on('input', function() {
                    $imageContainer.css('z-index', $(this).val());
                });

                $('#rotate').on('input', function() {
                    image.style.transform = `rotate(${$(this).val()}deg)`;
                });

                $('#apply-settings').off('click').on('click', function() {
                    $('#image-settings').hide();
                    $('.upload-wrapper').show();
                });

                $('#cancel-settings').off('click').on('click', function() {
                    $imageContainer.css('z-index', originalStyles.zIndex);
                    $(image).width(originalStyles.width);
                    $(image).height(originalStyles.height);
                    image.style.transform = `rotate(${originalStyles.rotate}deg)`;
                    $imageContainer.css('top', `${originalStyles.top}px`);
                    $imageContainer.css('left', `${originalStyles.left}px`);

                    $('#image-settings').hide();
                    $('.upload-wrapper').show();
                });
            });
        });



    }
});
