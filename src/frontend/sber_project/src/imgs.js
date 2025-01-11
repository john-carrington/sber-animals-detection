const carousel = document.querySelector(".carousel");
const backgroundImage = document.querySelector(".bg-image");
const leftArrow = document.querySelector(".left-arrow");
const rightArrow = document.querySelector(".right-arrow");
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const closeBtn = document.querySelector('.close');

let currentIndex = 0;
let prevIndex;
const images = document.querySelectorAll(".carousel-image");
const totalImages = images.length;
const imageWidth = 300;

leftArrow.addEventListener("click", () => {
    prevIndex = currentIndex;
    currentIndex = (currentIndex - 1 + totalImages) % totalImages;
    carousel.style.transform = `translateX(-${imageWidth}px)`;
    carousel.insertBefore(images[currentIndex], carousel.firstChild);

    setTimeout(() => {
        carousel.style.transform = "";
        carousel.classList.add("sliding-transition");
        backgroundImage.src = images[currentIndex].src.slice(0, -3) + "1000";
    }, 10);

    setTimeout(() => {
        carousel.classList.remove("sliding-transition");
    }, 490);
});

rightArrow.addEventListener("click", () => {
    carousel.classList.add("sliding-transition");

    prevIndex = currentIndex;
    currentIndex = (currentIndex + 1) % totalImages;

    carousel.style.transform = `translateX(-${imageWidth}px)`;
    backgroundImage.src = images[currentIndex].src.slice(0, -3) + "1000";

    setTimeout(() => {
        carousel.appendChild(images[prevIndex]);
        carousel.classList.remove("sliding-transition");
        carousel.style.transform = "";
    }, 500);
});

images.forEach(image => {
    image.addEventListener('click', function() {
        modal.style.display = 'block';
        modalImg.src = this.src;
    });
});

closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const files = fileInput.files;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const reader = new FileReader();

        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            preview.appendChild(img);
        };

        reader.readAsDataURL(file); 
    }

    // Здесь можно добавить код для отправки файлов на сервер
});






function reloadPage() {
  location.reload();
}