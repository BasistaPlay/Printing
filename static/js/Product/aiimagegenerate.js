const token = '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';
const InputTxt = document.getElementById('textInput-Ai');
const imagesContainer = document.getElementById('generatedImages');
const loader = document.getElementById('loader');

async function query() {
    if (!imagesContainer) return;

    imagesContainer.innerHTML = '';
    imagesContainer.style.pointerEvents = 'none';
    loader.style.display = 'block';

    for (let i = 0; i < 4; i++) {
        const imageBox = document.createElement('div');
        imageBox.className = 'image-box';
        imageBox.innerHTML = '<div class="loading-spinner"></div>';
        imagesContainer.appendChild(imageBox);

        try {
            const response = await fetch("https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image", {
                headers: { Authorization: `Bearer ${token}` },
                method: "POST",
                body: JSON.stringify({'inputs': InputTxt.value + `, variation ${i + 1}`}),
            });

            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            imageBox.innerHTML = '';
            addGeneratedImage(imageUrl, imageBox);
        } catch (error) {
            console.error("❌ Error fetching image:", error);
        }
    }

    loader.style.display = 'none';
    imagesContainer.style.pointerEvents = 'auto';
}


function addGeneratedImage(imageUrl, container) {
    const imgElement = document.createElement('img');
    imgElement.src = imageUrl;
    imgElement.className = 'generated-thumbnail';
    imgElement.onclick = () => addToProduct(imageUrl);
    container.appendChild(imgElement);
}

function addToProduct(imageUrl) {
    let currentSide = localStorage.getItem('currentSide') || 'front';
    const selectedContainer = document.getElementById(currentSide);

    if (!selectedContainer) {
        console.error("❌ Error: No active side selected!");
        return;
    }

    const imageId = Date.now();

    let htmlList = `
        <div class='uploaded-img ${currentSide}' data-image-id='${imageId}' id='save-img'>
            <img src='${imageUrl}' draggable='true' style='background: transparent; object-fit: contain;'>
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
            <img src='${imageUrl}' class='editable-image resizable-image' draggable='true' style='background: transparent; object-fit: contain;'>
        </div>
    `;
    selectedContainer.insertAdjacentHTML('afterbegin', htmlKrekls);

    $('.remove-btn').click(function () {
        let imageIdToRemove = $(this).parent().data('image-id');
        $('[data-image-id="' + imageIdToRemove + '"]').remove();
    });

    $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`).resizable({
        handles: 'ne, se, sw, nw, n, e, s, w',
        ghost: false,
        containment: `#boundary-${currentSide}`,
        // maxWidth: selectedContainer.width(),
        // maxHeight: selectedContainer.height()
    }).parent().draggable({
        containment: `#boundary-${currentSide}`
    });
}

document.getElementById('generateButton').addEventListener('click', query);

InputTxt.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        query();
    }
});
