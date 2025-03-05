document.addEventListener('DOMContentLoaded', function() {
    let currentSide = localStorage.getItem('currentSide') || 'front';
    localStorage.setItem('currentSide', currentSide);

    // Get elements and check if they exist
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

    // Function to hide content
    function hideContent(element) {
        if (element) {
            element.classList.add('hidden');
        }
    }

    // Function to show content
    function showContent(element) {
        if (element) {
            element.classList.remove('hidden');
        }
    }

    // Add event listeners only if elements exist
    if (generalIcon) {
        generalIcon.addEventListener('click', function() {
            showContent(generalContent);
            hideContent(uploadContent);
            hideContent(AiContent);
            hideContent(Text);
        });
    }

    if (textIcon) {
        textIcon.addEventListener('click', function() {
            showContent(Text);
            hideContent(uploadContent);
            hideContent(AiContent);
            hideContent(generalContent);
        });
    }

    if (imageIcon) {
        imageIcon.addEventListener('click', function() {
            showContent(uploadContent);
            hideContent(generalContent);
            hideContent(AiContent);
            hideContent(Text);
        });
    }

    if (ai) {
        ai.addEventListener('click', function() {
            showContent(AiContent);
            hideContent(generalContent);
            hideContent(uploadContent);
            hideContent(Text);
        });
    }

    if (rotate) {
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
    }


    var publishCheckbox = document.getElementById('publish-checkbox');
    var additionalInfo = document.getElementById('additional-info');

    publishCheckbox.addEventListener('change', function() {
        if (this.checked) {
            additionalInfo.class.display = 'block';
        } else {
            additionalInfo.class.display = 'hidden';
        }
    });

});
