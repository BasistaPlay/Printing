const showMenu = (toggleId,navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}
showMenu('nav-toggle','nav-menu')

const sizes = document.querySelectorAll('.size__tallas');
const colors = document.querySelectorAll('.sneaker__color');
const sneaker = document.querySelectorAll('.sneaker__img');

function changeSize(){
    sizes.forEach(size => size.classList.remove('active'));
    this.classList.add('active');
}

function changeColor(){
    let primary = this.getAttribute('primary');
    let color = this.getAttribute('color');
    let sneakerColor = document.querySelector(`.sneaker__img[color="${color}"]`);

    colors.forEach(c => c.classList.remove('active'));
    this.classList.add('active');

    document.documentElement.style.setProperty('--primary', primary);

    sneaker.forEach(s => s.classList.remove('shows'));
    sneakerColor.classList.add('shows')
}

sizes.forEach(size => size.addEventListener('click', changeSize));
colors.forEach(c => c.addEventListener('click', changeColor));

document.addEventListener('DOMContentLoaded', function () {
    const starWrapper = document.querySelector('.star-wrapper');
    const rating = parseFloat(starWrapper.getAttribute('data-rating'));
    const stars = starWrapper.querySelectorAll('.fas');

    stars.forEach(function (star, index) {
        const starValue = index + 1;

        if (starValue <= rating) {
            star.classList.add('active');
        } else if (starValue - 0.5 === rating) {
            star.classList.add('active-half');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var img = document.getElementById('sneakerImg');

    if (img) {
        var canvas = document.getElementById('outputCanvas');
        var ctx = canvas.getContext('2d');

        if (canvas && ctx) {
            canvas.width = img.width;
            canvas.height = img.height;

            ctx.drawImage(img, 0, 0);

            var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            var data = imageData.data;

            var backgroundColor = [255, 255, 255];

            for (var i = 0; i < data.length; i += 4) {
                if (data[i] === backgroundColor[0] && data[i + 1] === backgroundColor[1] && data[i + 2] === backgroundColor[2]) {
                    data[i + 3] = 0;
                }
            }

            ctx.putImageData(imageData, 0, 0);
            var outputImg = new Image();
            outputImg.src = canvas.toDataURL();

            var img2 = document.getElementById('sneakerImg2');
            var canvas2 = document.getElementById('outputCanvas2');
            var ctx2 = canvas2.getContext('2d');

            if (canvas2 && ctx2 && img2) {
                canvas2.width = img2.width;
                canvas2.height = img2.height;

                ctx2.drawImage(img2, 0, 0);

                var imageData2 = ctx2.getImageData(0, 0, canvas2.width, canvas2.height);
                var data2 = imageData2.data;

                var backgroundColor2 = [255, 255, 255];

                for (var j = 0; j < data2.length; j += 4) {
                    if (data2[j] === backgroundColor2[0] && data2[j + 1] === backgroundColor2[1] && data2[j + 2] === backgroundColor2[2]) {
                        data2[j + 3] = 0;
                    }
                }

                ctx2.putImageData(imageData2, 0, 0);
            } else {
                console.error('Canvas element not found or getContext() not supported');
            }
        } else {
            console.error('Canvas element not found or getContext() not supported');
        }
    } else {
        console.error('Image element not found');
    }
});