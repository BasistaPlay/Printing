// -----------Color-----------

document.addEventListener('DOMContentLoaded', function() {
  var colorElements = document.querySelectorAll('.color-select');
  var colorContainer = document.querySelector('.color');

  colorElements.forEach(function(colorElement, index) {
    colorElement.addEventListener('click', function() {
      var selectedColor = colorElement.style.backgroundColor;

      colorContainer.style.backgroundColor = selectedColor;

      colorElements.forEach(function(element) {
        element.classList.remove('active-color');
      });
      colorElement.classList.add('active-color');
    });
  });
});

// -----------Image-----------

$(document).ready(function () {
  let currentSide = localStorage.getItem('currentSide') || 'front'; // Get the current side from localStorage or default to 'front'

  $('.upload-area').click(function () {
    $('#upload-input').trigger('click');
  });

  $('#upload-input').change(event => {
    if (event.target.files) {
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
            <div class='uploaded-img ${currentSide}' data-image-id='${imageId}'>
              <img src='${event.target.result}' class='editable-image' draggable='true'>
              <button type='button' class='remove-btn'>
                <i class='fas fa-times'></i>
              </button>
            </div>
          `;
          $('.upload-img').append(htmlList);

          let htmlKrekls = `
            <div class='uploaded-img element-image ${currentSide}' data-image-id='${imageId}'>
              <img src='${event.target.result}' class='editable-image' draggable='true'>
            </div>
          `;
          let selectedContainer;
          if (currentSide === 'front') {
            selectedContainer = $('#front');
          } else {
            selectedContainer = $('#back');
          }
          selectedContainer.append(htmlKrekls);

          let editableImage = selectedContainer.find('.editable-image');

          editableImage.on('click', function () {
            rotateImage($(this));
          });

          $('.remove-btn').click(function () {
            let imageIdToRemove = $(this).parent().data('image-id');
            $('[data-image-id="' + imageIdToRemove + '"]').remove();
          });

          // Make the image draggable using jQuery UI
          $('.editable-image').draggable();
        };
        reader.readAsDataURL(files[i]);
      }

      $('.upload-img').css('padding', '20px');
    }
  }

  $('.remove-btn').click(function () {
    let imageIdToRemove = $(this).parent().data('image-id');
    $('[data-image-id="' + imageIdToRemove + '"]').remove();
  });

  const generalContent = document.getElementById('general');
  const uploadContent = document.getElementById('upload');
  const AiContent = document.getElementById('Ai-generator');
  const Text = document.getElementById('Text');
  const Back = document.getElementById('back');
  const Front = document.getElementById('front');

  const generalIcon = document.getElementById('generalIcon');
  const imageIcon = document.getElementById('imageIcon');
  const textIcon = document.getElementById('textIcon');
  const ai = document.getElementById('Ai-generatoricon');
  const rotate = document.getElementById('roatateicon');

  generalIcon.addEventListener('click', function () {
    showContent(generalContent);
    hideContent(uploadContent);
    hideContent(AiContent);
    hideContent(Text);
  });

  textIcon.addEventListener('click', function () {
    showContent(Text);
    hideContent(uploadContent);
    hideContent(AiContent);
    hideContent(generalContent);
  });

  imageIcon.addEventListener('click', function () {
    showContent(uploadContent);
    hideContent(generalContent);
    hideContent(AiContent);
    hideContent(Text);
  });

  ai.addEventListener('click', function () {
    showContent(AiContent);
    hideContent(generalContent);
    hideContent(uploadContent);
    hideContent(Text);
  });

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

    // Save the current side to localStorage
    localStorage.setItem('currentSide', currentSide);
  });

  function hideContent(element) {
    element.style.display = 'none';
  }

  function showContent(element) {
    element.style.display = 'block';
  }
});



  // -----------Text-----------

let editingIndex = -1;

function addText() {
  const textInput = document.getElementById('text-input');
  const textList = document.getElementById('text-list');
  const fontSize = document.getElementById('font-size').value + 'px';
  const editButton = document.getElementById('button');

  editButton.innerHTML = '<i class="fas fa-plus"></i> Add text';

  const text = textInput.value.trim();

  if (text !== '') {
      if (editingIndex === -1) {
          const textContainer = document.getElementById('text-container');
          const textElement = document.createElement('div');
          textElement.innerHTML = `<span style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value};">${text}</span>`;
          const listItem = document.createElement('li');
          listItem.className = 'text-list-item';
          textContainer.appendChild(textElement);
          listItem.innerHTML = `
              <span style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value};">${text}</span>
              <button class="edit-button" onclick="editTextInList(this)"><i class="fas fa-edit"></i></button>
              <button class="delete-button" onclick="deleteText(this)"><i class="fas fa-trash-alt"></i></button>
          `;

          textList.appendChild(listItem);

          // Pievienot notikumu klausītāju "drag" un "dragstart"
          textElement.setAttribute('draggable', 'true');
          textElement.setAttribute('ondragstart', 'drag(event)');
      } else {
          const editedItem = textList.children[editingIndex];
          const textSpan = editedItem.querySelector('span');

          textSpan.innerHTML = text;
          textSpan.style.fontSize = fontSize;
          textSpan.style.color = document.getElementById('font-color').value;
          textSpan.style.fontFamily = document.getElementById('font-select').value;

          // Update text on T-shirt image
          const textContainer = document.getElementById('text-container');
          const editedElement = textContainer.children[editingIndex];
          editedElement.innerHTML = `<span style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value};">${text}</span>`;

          // Pievienot notikumu klausītāju "drag" un "dragstart" tikai uz attēla elementu
          editedElement.firstChild.setAttribute('draggable', 'true');
          editedElement.firstChild.setAttribute('ondragstart', 'drag(event)');

          editingIndex = -1;
      }

      textInput.value = '';
  } else {
      alert('Please enter text before adding to the list.');
  }
}

    function editTextInList(button) {
      const listItem = button.parentNode;
      const textSpan = listItem.querySelector('span');
      const textInput = document.getElementById('text-input');
      const textContainer = document.getElementById('text-container');
      const editButton = document.getElementById('button');

      editButton.innerHTML = '<i class="fas fa-edit"></i> Edit text';
  
      textInput.value = textSpan.textContent;
      document.getElementById('font-select').value = textSpan.style.fontFamily;
      document.getElementById('font-size').value = parseInt(textSpan.style.fontSize);
      document.getElementById('font-color').value = textSpan.style.color;
      editingIndex = Array.from(listItem.parentNode.children).indexOf(listItem);
  
      // Update only the selected text in text-container
      const editedElement = textContainer.children[editingIndex];
      editedElement.innerHTML = `<span style="font-size: ${textSpan.style.fontSize}; color: ${textSpan.style.color}; font-family: ${textSpan.style.fontFamily};">${textSpan.textContent}</span>`;
  }

    function deleteText(button) {
      const listItem = button.parentNode;
      const textList = document.getElementById('text-list');
      const textContainer = document.getElementById('text-container');
  
      listItem.remove();
      textContainer.innerHTML = ""; // Notīra reklāmas attēlu
  
      // Pārvieto tekstu no saraksta uz reklāmas attēlu
      for (let i = 0; i < textList.children.length; i++) {
          const listItem = textList.children[i];
          const textSpan = listItem.querySelector('span');
  
          const textElement = document.createElement('div');
          textElement.innerHTML = `<span style="font-size: ${textSpan.style.fontSize}; color: ${textSpan.style.color}; font-family: ${textSpan.style.fontFamily};">${textSpan.textContent}</span>`;
          textContainer.appendChild(textElement);
      }
  
      editingIndex = -1;
  }
  function drag(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

// Notikumu klausītāji "dragover", "dragenter", "dragleave", un "drop"
$('#front, #back').on('dragover dragenter', function (event) {
    event.preventDefault();
});

$('#front, #back').on('dragleave', function (event) {
    // Iztīrīt jebkuru klasi vai vizuālo efektu, ja pārvietojat pāri elementam un pēc tam aizietat
});

$('#front, #back').on('drop', function (event) {
    event.preventDefault();
    let data = event.dataTransfer.getData('text/plain');
    let draggedElement = document.getElementById(data);

    // Pārbaudīt, vai pārvietotais elements ir T-krekls
    if (draggedElement.closest('#front, #back')) {
        let currentSide = getCurrentSide();
        let selectedContainer;

        if (currentSide === 'front') {
            selectedContainer = $('#front');
        } else {
            selectedContainer = $('#back');
        }

        selectedContainer.append(draggedElement);
    }
});
