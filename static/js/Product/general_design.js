import $ from 'jquery';

document.addEventListener('DOMContentLoaded', function() {
    const colorElements = document.querySelectorAll('#color-select');
    const colorContainer = document.querySelector('.color');

    colorElements.forEach(function(colorElement) {
        colorElement.addEventListener('click', function() {
            const selectedColor = colorElement.style.backgroundColor;
            if (colorContainer) {
                colorContainer.style.backgroundColor = selectedColor;
            }

            colorElements.forEach(function(element) {
                element.classList.remove('ring-2', 'ring-offset-2', 'ring-gray-800', 'active-color');
            });

            colorElement.classList.add('ring-2', 'ring-offset-2', 'ring-gray-800', 'active-color');

            const colorId = colorElement.getAttribute('data-color-id');
            const productSlug = document.getElementById('product-slug').value;
        });
    });


    const sizeOptions = document.querySelectorAll('.size-option');
    sizeOptions.forEach(option => {
        option.addEventListener('click', function() {
            if (!option.classList.contains('readonly')) {
                sizeOptions.forEach(opt => opt.classList.remove('active'));
                option.classList.add('active');
            }
        });
    });

    const checkbox = document.getElementById("publish-checkbox");
    const additionalInfo = document.getElementById("additional-info");

    if (checkbox && additionalInfo) {
        checkbox.addEventListener("change", function () {
            additionalInfo.classList.toggle("hidden", !this.checked);
        });
    }

    function bindQuantityControls() {
        document.querySelectorAll('.qty-control').forEach(wrapper => {
            const input = wrapper.querySelector('input[type="number"]');
            const plus = wrapper.querySelector('.plus');
            const minus = wrapper.querySelector('.minus');

            let value = parseInt(input.value) || 0;

            function updateDisplay() {
                input.value = value;
            }

            if (plus) {
                plus.addEventListener('click', () => {
                    value++;
                    updateDisplay();
                });
            }

            if (minus) {
                minus.addEventListener('click', () => {
                    if (value > 0) {
                        value--;
                        updateDisplay();
                    }
                });
            }

            updateDisplay();
        });
    }

    bindQuantityControls();
});
