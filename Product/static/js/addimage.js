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
                            <svg width="20" height="20" style="color: var(--main-color);">
                                <use xlink:href="/static/svg/sprite.svg#x-circle"></use>
                            </svg>
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
});