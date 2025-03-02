document.addEventListener('DOMContentLoaded', function() {
    const colorElements = document.querySelectorAll('.color-select');
    const colorContainer = document.querySelector('.color');

    colorElements.forEach(function(colorElement) {
        colorElement.addEventListener('click', function() {
            const selectedColor = colorElement.style.backgroundColor;
            colorContainer.style.backgroundColor = selectedColor;

            colorElements.forEach(function(element) {
                element.classList.remove('active-color');
            });
            colorElement.classList.add('active-color');

            const colorId = colorElement.getAttribute('data-color-id');
            const productSlug = document.getElementById('product-slug').value;

            fetch(`/product/design/${productSlug}/?color_id=${colorId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                const contentType = response.headers.get('content-type');
                if (!response.ok || !contentType || !contentType.includes('application/json')) {
                    throw new Error('Invalid JSON response');
                }
                return response.json();
            })
            .then(data => {
                const sizesMap = new Map();
                data.sizes.forEach(size => {
                    sizesMap.set(size.size__size, size.quantity);
                });

                const sizeOptions = document.querySelectorAll('.size-option');
                sizeOptions.forEach(option => {
                    const sizeName = option.getAttribute('data-size');
                    option.classList.remove('readonly');
                    option.classList.remove('active');
                    option.style.pointerEvents = 'auto';

                    const quantity = sizesMap.get(sizeName);
                    if (quantity === undefined || quantity === 0) {
                        option.classList.add('readonly');
                        option.style.pointerEvents = 'none';
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching sizes:', error);
            });
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

    const plus = document.querySelector(".plus"),
        minus = document.querySelector(".minus"),
        num = document.querySelector(".num");

    let a = 1;

    function updateNumDisplay() {
        num.innerText = a < 10 ? '0' + a : a;
    }

    plus.addEventListener('click', () => {
        a++;
        updateNumDisplay();
    });

    minus.addEventListener('click', () => {
        if (a > 1) {
            a--;
            updateNumDisplay();
        }
    });

    updateNumDisplay();

    var infoIcon = document.querySelector('.info-icon');
    var modal = document.getElementById('info-modal');
    var closeBtn = document.querySelector('.close');

    infoIcon.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});