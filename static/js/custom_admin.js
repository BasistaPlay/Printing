document.addEventListener('DOMContentLoaded', function() {
    let fabricCanvasFront = setupCanvas('id_front_image_not_background', 'id_front_image_coords', 400, 400);
    let fabricCanvasBack = setupCanvas('id_back_image_not_background', 'id_back_image_coords', 400, 400);

    function setupCanvas(imageFieldId, coordsFieldId, fixedWidth, fixedHeight) {
        const imageField = document.getElementById(imageFieldId);
        if (!imageField) return null;

        const canvasContainer = document.createElement('div');
        canvasContainer.classList.add('canvas-container');
        imageField.parentNode.insertBefore(canvasContainer, imageField);

        const canvas = document.createElement('canvas');
        canvasContainer.appendChild(canvas);

        const fabricCanvas = new fabric.Canvas(canvas);
        const coordsField = document.getElementById(coordsFieldId);
        let activeRect = null;

        // Function to load image onto the canvas
        function loadImage(imageUrl) {
            const image = new Image();
            image.src = imageUrl;

            image.onload = function() {
                fabricCanvas.setWidth(fixedWidth);
                fabricCanvas.setHeight(fixedHeight);
                const fabricImage = new fabric.Image(image, {
                    scaleX: fixedWidth / image.width,
                    scaleY: fixedHeight / image.height
                });
                fabricCanvas.setBackgroundImage(fabricImage, fabricCanvas.renderAll.bind(fabricCanvas));

                // Remove the active rectangle if it exists
                if (activeRect) {
                    fabricCanvas.remove(activeRect);
                    activeRect = null;
                }

                // Restore existing coordinates if present
                if (coordsField.value && coordsField.value !== 'null') {
                    const coords = JSON.parse(coordsField.value);
                    activeRect = new fabric.Rect({
                        left: coords.left,
                        top: coords.top,
                        width: coords.width,
                        height: coords.height,
                        fill: 'rgba(255, 0, 0, 0.5)',
                        selectable: false
                    });
                    fabricCanvas.add(activeRect);
                }
            };
        }

        // Load the initial image if it exists
        const initialImageUrl = imageField.parentNode.querySelector('a')?.href;
        if (initialImageUrl) {
            loadImage(initialImageUrl);
        }

        // Event listener for image field change
        imageField.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    loadImage(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });

        // Drawing functionality
        fabricCanvas.on('mouse:down', function(opt) {
            const pointer = fabricCanvas.getPointer(opt.e);

            if (activeRect) {
                fabricCanvas.remove(activeRect);
            }

            const rect = new fabric.Rect({
                left: pointer.x,
                top: pointer.y,
                width: 0,
                height: 0,
                fill: 'rgba(255, 0, 0, 0.5)',
                selectable: false
            });

            fabricCanvas.add(rect);
            fabricCanvas.setActiveObject(rect);
            activeRect = rect;

            fabricCanvas.on('mouse:move', function(opt) {
                const pointer = fabricCanvas.getPointer(opt.e);
                const rect = activeRect;
                if (!rect) return;

                rect.set({
                    width: Math.abs(pointer.x - rect.left),
                    height: Math.abs(pointer.y - rect.top)
                });

                fabricCanvas.renderAll();
            });

            fabricCanvas.on('mouse:up', function() {
                fabricCanvas.off('mouse:move');
                fabricCanvas.off('mouse:up');

                const rect = activeRect;
                if (!rect) return;

                const coords = {
                    left: rect.left,
                    top: rect.top,
                    width: rect.width,
                    height: rect.height
                };
                coordsField.value = JSON.stringify(coords);
            });
        });

        fabricCanvas.on('object:modified', function(opt) {
            const rect = opt.target;
            if (rect && rect === activeRect) {
                const coords = {
                    left: rect.left,
                    top: rect.top,
                    width: rect.width,
                    height: rect.height
                };
                coordsField.value = JSON.stringify(coords);
            }
        });

        return fabricCanvas;
    }
});