document.addEventListener('DOMContentLoaded', function() {
  var colorElements = document.querySelectorAll('.color-select');
  var colorContainer = document.querySelector('.color'); // Assuming .color is the element you want to change

  colorElements.forEach(function(colorElement, index) {
    colorElement.addEventListener('click', function() {
      // Pārliecināsimies, ka ieklikšķinātā krāsa ir pareizi atlasīta
      var selectedColor = colorElement.style.backgroundColor;

      // Nomainīsim krāsu elementam ar klasi "color"
      colorContainer.style.backgroundColor = selectedColor;

      // Norādīsim, kura krāsa ir izvēlēta, pieliekot klasi "active-color"
      colorElements.forEach(function(element) {
        element.classList.remove('active-color');
      });
      colorElement.classList.add('active-color');
    });
  });
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
      
          $('.upload-img').css('padding', '20px');
        }
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
let editingIndex = -1; // Uzglabā rediģējamā teksta indeksu

    function addText() {
        const textInput = document.getElementById('text-input');
        const textList = document.getElementById('text-list');
        const fontSize = document.getElementById('font-size').value + 'px';
        // const fontStyle = document.querySelector('input[name="font-style"]:checked').value;

        const text = textInput.value.trim(); // Izņemam tukšumus no sākuma un beigām

        if (text !== '') {
            if (editingIndex === -1) {
                // Ja netiek rediģēts teksts, pievieno jaunu
                const listItem = document.createElement('li');
                listItem.className = 'text-list-item';

                listItem.innerHTML = `
                    <span style="font-size: ${fontSize}; color: ${document.getElementById('font-color').value}; font-family: ${document.getElementById('font-select').value};">${text}</span>
                    <button class="edit-button" onclick="editTextInList(this)"><i class="fas fa-edit"></i></button>
                    <button class="delete-button" onclick="deleteText(this)"><i class="fas fa-trash-alt"></i></button>
                `;

                textList.appendChild(listItem);
            } else {
                // Ja tiek rediģēts teksts, atjauno esošo
                const editedItem = textList.children[editingIndex];
                const textSpan = editedItem.querySelector('span');

                textSpan.innerHTML = text;
                textSpan.style.fontSize = fontSize;
                textSpan.style.color = document.getElementById('font-color').value;
                textSpan.style.fontFamily = document.getElementById('font-select').value;
                // textSpan.style.fontStyle = fontStyle;

                editingIndex = -1; // Atiestata rediģēšanas indeksu
            }

            textInput.value = '';
            updateFontPreview();
        } else {
            alert('Please enter text before adding to the list.');
        }
    }

    function editTextInList(button) {
        const listItem = button.parentNode;
        const textSpan = listItem.querySelector('span');
        const textInput = document.getElementById('text-input');

        textInput.value = textSpan.textContent;
        document.getElementById('font-select').value = textSpan.style.fontFamily; // Iestata fontu izvēlnē
        document.getElementById('font-size').value = parseInt(textSpan.style.fontSize);
        document.getElementById('font-color').value = textSpan.style.color;

        // const fontStyle = textSpan.style.fontStyle;
        // document.querySelector(`input[name="font-style"][value="${fontStyle}"]`).checked = true;

        // Iegūst rediģējamā teksta indeksu
        editingIndex = Array.from(listItem.parentNode.children).indexOf(listItem);

        updateFontPreview();
    }

    function deleteText(button) {
        const listItem = button.parentNode;
        listItem.remove();
        editingIndex = -1; // Atiestata rediģēšanas indeksu
    }

    function updateFontPreview() {
        const selectedFont = document.getElementById('font-select').value;
        const fontPreview = document.getElementById('output-text');
        fontPreview.style.fontFamily = selectedFont;
    }

    function editText() {
        const textInput = document.getElementById('text-input');
        const fontPreview = document.getElementById('output-text');

        const textList = document.getElementById('text-list');
        const editedItem = textList.children[editingIndex];
        const textSpan = editedItem.querySelector('span');

        textSpan.innerHTML = textInput.value.trim();
        textSpan.style.fontSize = document.getElementById('font-size').value + 'px';
        textSpan.style.color = document.getElementById('font-color').value;
        textSpan.style.fontFamily = document.getElementById('font-select').value;
        // textSpan.style.fontStyle = document.querySelector('input[name="font-style"]:checked').value;

        editingIndex = -1; // Atiestata rediģēšanas indeksu
        textInput.value = '';
        updateFontPreview();
    }
