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
    let initialDistance = 0;
    let initialScale = 1;

    $(document).on('mousedown touchstart', '.editable-image', function(event) {
        if (resizableElement && !$(this).is(resizableElement)) {
            resizableElement.resizable("destroy");
        }

        // Make image resizable
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

        // Make image draggable
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

        // Handle touch events
        $(this).on('touchmove', function(event) {
            event.preventDefault();
            let wrapper = $(this).parent();

            if (event.originalEvent.touches.length === 1) {
                let touch = event.originalEvent.touches[0];
                let boundary = $(`#boundary-${currentSide}`);
                let boundaryOffset = boundary.offset();
                let boundaryWidth = boundary.width();
                let boundaryHeight = boundary.height();

                let newLeft = touch.pageX - wrapper.outerWidth() / 2;
                let newTop = touch.pageY - wrapper.outerHeight() / 2;

                if (newLeft < boundaryOffset.left) {
                    newLeft = boundaryOffset.left;
                }
                if (newTop < boundaryOffset.top) {
                    newTop = boundaryOffset.top;
                }
                if (newLeft + wrapper.outerWidth() > boundaryOffset.left + boundaryWidth) {
                    newLeft = boundaryOffset.left + boundaryWidth - wrapper.outerWidth();
                }
                if (newTop + wrapper.outerHeight() > boundaryOffset.top + boundaryHeight) {
                    newTop = boundaryOffset.top + boundaryHeight - wrapper.outerHeight();
                }

                wrapper.css({
                    top: newTop,
                    left: newLeft
                });
            }

            // Handle pinch-to-zoom gesture
            if (event.originalEvent.touches.length === 2) {
                let touch1 = event.originalEvent.touches[0];
                let touch2 = event.originalEvent.touches[1];

                let currentDistance = Math.hypot(
                    touch2.pageX - touch1.pageX,
                    touch2.pageY - touch1.pageY
                );

                if (initialDistance === 0) {
                    initialDistance = currentDistance;
                }

                let scale = currentDistance / initialDistance;

                wrapper.css({
                    transform: `scale(${scale * initialScale})`
                });

                event.stopPropagation();
            }
        });

        // Reset initial variables on touch end
        $(this).on('touchend', function(event) {
            initialScale *= parseFloat(wrapper.css('transform').split('(')[1]);
            initialDistance = 0;
            wrapper.css({
                transform: `scale(1)` // Reset the transform
            });
        });
    });

    $(document).on('click', '.remove-btn', function() {
        let imageIdToRemove = $(this).parent().data('image-id');
        $('[data-image-id="' + imageIdToRemove + '"]').remove();
    });

    $(document).on('mousedown touchstart', function(event) {
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

                // Support for touch events on new images
                $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`).on('touchmove', function(event) {
                    event.preventDefault();
                    let wrapper = $(this).parent();
                    let newLeft = touch.pageX - wrapper.width() / 2;
                    let newTop = touch.pageY - wrapper.height() / 2;

                    // Check boundaries
                    let boundary = $(`#boundary-${currentSide}`);
                    let boundaryOffset = boundary.offset();
                    let boundaryWidth = boundary.width();
                    let boundaryHeight = boundary.height();

                    if (newLeft < boundaryOffset.left) {
                        newLeft = boundaryOffset.left;
                    }
                    if (newTop < boundaryOffset.top) {
                        newTop = boundaryOffset.top;
                    }
                    if (newLeft + wrapper.width() > boundaryOffset.left + boundaryWidth) {
                        newLeft = boundaryOffset.left + boundaryWidth - wrapper.width();
                    }
                    if (newTop + wrapper.height() > boundaryOffset.top + boundaryHeight) {
                        newTop = boundaryOffset.top + boundaryHeight - wrapper.height();
                    }

                    wrapper.css({
                        top: newTop,
                        left: newLeft
                    });
                });
            };
            reader.readAsDataURL(files[i]);
        }

        $('.upload-img').css('padding', '20px');
    }

    $('.remove-btn').click(function() {
        let imageIdToRemove = $(this).parent().data('image-id');
        $('[data-image-id="' + imageIdToRemove + '"]').remove();
    });
}
});
