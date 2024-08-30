const token = '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';
const InputTxt = document.getElementById('textInput-Ai');
const image = document.getElementById('image');
const button = document.getElementById('generateButton');
const loader = document.getElementById('loader');

async function query() {
    loader.style.display = 'block';

    const response = await fetch(
        "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image",
        {
            headers: { Authorization: `Bearer ${token}` },
            method: "POST",
            body: JSON.stringify({'inputs': InputTxt.value}),
        }
    );
    const result = await response.blob();

    loader.style.display = 'none';

    image.onload = function() {
        document.getElementById('sendToImageBtn').style.display = 'flex';
    };

    image.src = URL.createObjectURL(result);
}

button.addEventListener('click', async function(){
    document.getElementById('sendToImageBtn').style.display = 'none';
    query();
});

document.getElementById('sendToImageBtn').addEventListener('click', function() {
    const imageContainer = document.getElementById('image');
    const uploadImgContainer = document.querySelector('.upload-img');
    const imageId = Date.now();

    let selectedContainer;
    const frontContainer = document.getElementById('front');
    const backContainer = document.getElementById('back');

    if (frontContainer.style.display === 'block') {
        selectedContainer = frontContainer;
    } else {
        selectedContainer = backContainer;
    }

    if (selectedContainer) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = imageContainer.width;
        canvas.height = imageContainer.height;
        ctx.drawImage(imageContainer, 0, 0, canvas.width, canvas.height);
        const base64data = canvas.toDataURL();

        const sideId = selectedContainer.id;

        const newImg = document.createElement('img');
        newImg.className = 'uploaded-img element-image resizable-image';
        newImg.src = base64data;

        const htmlImage = `
            <div class='uploaded-img element-image ${sideId} ui-wrapper' style='z-index:2; top:100px; background: transparent;' data-image-id='${imageId}'>
                <img src='${base64data}' class='editable-image resizable-image' draggable='true'>
            </div>
        `;

        selectedContainer.insertAdjacentHTML('afterbegin', htmlImage);

        let $resizableImage = $(`.uploaded-img[data-image-id='${imageId}'] .editable-image`);
        $resizableImage.resizable({
            containment: `#boundary-${sideId}`,
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
            containment: `#boundary-${sideId}`,
            ghost: false,
            stop: function(event, ui) {
                let wrapper = ui.helper;
                wrapper.css({
                    top: ui.position.top,
                    left: ui.position.left,
                });
            }
        });
    } else {
        const errorMessage = document.getElementById('error-messages');
        errorMessage.innerText = 'Nevarēja noteikt aktīvo pusi. Lūdzu, izvēlieties aktīvo pusi, kurai pievienot attēlu.';
        errorMessage.style.display = 'block';
    }
    const canvas2 = document.createElement('canvas');
    const ctx2 = canvas2.getContext('2d');
    canvas2.width = imageContainer.width;
    canvas2.height = imageContainer.height;
    ctx2.drawImage(imageContainer, 0, 0, canvas2.width, canvas2.height);
    const base64data2 = canvas2.toDataURL();

    const newImg2 = document.createElement('img');
    newImg2.className = 'uploaded-img front';
    newImg2.src = base64data2;

    const newDiv2 = document.createElement('div');
    newDiv2.className = 'uploaded-image-container';
    newDiv2.id = 'save-img';
    newDiv2.setAttribute('data-image-id', imageId)

    const removeBtn2 = document.createElement('button');
    removeBtn2.type = 'button';
    removeBtn2.className = 'remove-btn';
    removeBtn2.innerHTML = '<svg width="20" height="20" style="color: var(--main-color);"><use xlink:href="/static/svg/sprite.svg#x-circle"></use></svg>';
    removeBtn2.addEventListener('click', function() {
        let imageIdToRemove = $(this).parent().data('image-id');
        $(`[data-image-id="${imageIdToRemove}"]`).remove();

        let listItemToRemove = $('.text-list-item').eq(imageIdToRemove);
        listItemToRemove.remove();
    });
    newDiv2.appendChild(newImg2);
    newDiv2.appendChild(removeBtn2);

    uploadImgContainer.appendChild(newDiv2);

});

