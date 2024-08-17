document.addEventListener('DOMContentLoaded', function() {
    // Nolasīt JSON datus no HTML elementa
    const colorSizeMapElement = document.getElementById('color-size-map');
    window.colorSizeMap = JSON.parse(colorSizeMapElement.getAttribute('data-color-size-map'));

    // Pārliecinies, ka datos nav kļūdu
    console.log('Color Size Map:', window.colorSizeMap);

    const colorSelects = document.querySelectorAll('.color-select');
    const sizeOptions = document.querySelectorAll('.size-option');

    function updateSizeOptions() {
        const selectedColor = document.querySelector('.color-select.selected');
        const selectedColorName = selectedColor ? selectedColor.getAttribute('data-color-name') : null;

        console.log('Selected Color:', selectedColorName);

        // Pārliecinies, ka izmēru opcijas ir pieejamas
        sizeOptions.forEach(option => {
            option.classList.add('disabled');
            option.setAttribute('disabled', 'true');
        });

        if (selectedColorName) {
            const availableSizes = window.colorSizeMap[selectedColorName]?.sizes || [];

            console.log('Available Sizes:', availableSizes);

            sizeOptions.forEach(option => {
                const size = option.textContent.trim();
                console.log('Size:', size); // Pārliecinies par tekstu
                if (availableSizes.includes(size)) {
                    option.classList.remove('disabled');
                    option.removeAttribute('disabled');
                }
            });
        }
    }

    colorSelects.forEach(select => {
        select.addEventListener('click', function() {
            colorSelects.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');

            updateSizeOptions();
        });
    });

    updateSizeOptions();
});