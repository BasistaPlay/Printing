// Get elements from the DOM
const color = document.querySelector(".color");
const colorInput = document.querySelector(".color-input");
const imgElement = document.getElementById('img-1');
const imageContainer = document.querySelector('.image-container');

// Add input event listener for color change
colorInput.addEventListener("input", () => {
    color.style.backgroundColor = colorInput.value;
});



// Additional color change functionality (optional)
document.querySelector('.color-input').addEventListener('input', function (e) {
    const color = e.target.value;
    document.querySelector('.color').style.backgroundColor = color;
});



    $(document).ready(function(){
      $('.upload-area').click(function(){
        $('#upload-input').trigger('click');
      });
      
      $('#upload-input').change(event => {
        if(event.target.files){
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

      // funkcija, kas apstrādā augšupielādētos failus
      function handleFiles(files) {
        if (files) {
          let filesAmount = files.length;
      
          for (let i = 0; i < filesAmount; i++) {
            let reader = new FileReader();
            reader.onload = function(event) {
              let html = `
                <div class='uploaded-img'>
                  <img src='${event.target.result}'>
                  <button type='button' class='remove-btn'>
                    <i class='fas fa-times'></i>
                  </button>
                </div>
              `;
              $('.upload-img').append(html);
            };
            reader.readAsDataURL(files[i]);
          }
      
          updateUploadedFilesCount(); // Jaunais izsaukums, lai atjauninātu failu skaitu
      
          $('.upload-img').css('padding', '20px');
        }
      }
      
      // funkcija, kas atjaunina augšupielādēto failu skaitu teksta laukā
      function updateUploadedFilesCount() {
        let uploadedFilesCount = $('.uploaded-img').length;
        $('.upload-info-value').text(uploadedFilesCount + 1 );
      }

      $(window).click(function(event) {
        if($(event.target).hasClass('remove-btn')){
          $(event.target).parent().remove();
        } else if($(event.target).parent().hasClass('remove-btn')){
          $(event.target).parent().parent().remove();
        }
      });
    });



    document.addEventListener('DOMContentLoaded', function () {
      const generalContent = document.getElementById('general');
      const uploadContent = document.getElementById('upload');
      const AiContent = document.getElementById('Ai-generator');
      const Text = document.getElementById('Text');
      const Back = document.getElementById('back');
      const Front = document.getElementById('front');
      
      const generalIcon = document.getElementById('generalIcon');
      const imageIcon = document.getElementById('imageIcon');
      const textIcon = document.getElementById('textIcon');
      const ai = document.getElementById('Ai-generatoricon')
      const rotate = document.getElementById('roatateicon')

  
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
      if (Front.style.display === 'block') {
        showContent(Back);
        hideContent(Front);
      } else {
        showContent(Front);
        hideContent(Back);
      }
    });

      function hideContent(element) {
          element.style.display = 'none';
      }
  
      function showContent(element) {
          element.style.display = 'block';
      }
  });



// Text settings
document.getElementById('font-select').addEventListener('change', updateFontPreview);

    function updateFontPreview() {
        const selectedFont = document.getElementById('font-select').value;
        const fontPreview = document.getElementById('output-text');
        fontPreview.style.fontFamily = selectedFont;
    }

    function addText() {
        const textInput = document.getElementById('text-input');
        const fontPreview = document.getElementById('output-text');
        const textList = document.getElementById('text-list');

        const text = textInput.value;

        const listItem = document.createElement('li');
        listItem.className = 'text-list-item';

        listItem.innerHTML = `
            <span style="font-family: ${fontPreview.style.fontFamily}; font-size: ${document.getElementById('font-size').value}px; color: ${document.getElementById('font-color').value};">${text}</span>
            <button onclick="editTextInList(this)">Edit</button>
            <button onclick="deleteText(this)">Delete</button>
        `;

        textList.appendChild(listItem);
        textInput.value = '';
        updateFontPreview(); // Lai atjaunotu ar noklusējuma stilu
    }

    function editText() {
        const textInput = document.getElementById('text-input');
        const fontPreview = document.getElementById('output-text');

        textInput.value = fontPreview.textContent;
        updateFontPreview();
    }

    function editTextInList(button) {
        const listItem = button.parentNode;
        const textSpan = listItem.querySelector('span');
        const textInput = document.getElementById('text-input');

        textInput.value = textSpan.textContent;
        updateFontPreview();

        listItem.remove();
    }

    function deleteText(button) {
        const listItem = button.parentNode;
        listItem.remove();
    }