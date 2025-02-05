// Array of image sources
const images = ["headphones1.jpg", "headphones2.jpg", "headphones3.jpg"];
let currentIndex = 0;

// Get elements
const headphoneImage = document.getElementById('headphoneImage');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// Function to change image
function updateImage(index) {
    headphoneImage.src = images[index];
}

// Event listeners for buttons
prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex === 0) ? images.length - 1 : currentIndex - 1;
    updateImage(currentIndex);
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex === images.length - 1) ? 0 : currentIndex + 1;
    updateImage(currentIndex);
});
