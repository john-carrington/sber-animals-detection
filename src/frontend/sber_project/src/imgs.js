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

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы
  
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const files = fileInput.files;
    const formData = new FormData();
  
    // Добавляем файлы в FormData
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        formData.append('files', file);
  
        // Отображаем предварительный просмотр изображений
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            preview.appendChild(img);
        };
        reader.readAsDataURL(file);
    }
  
    // Отправляем файлы на сервер
    try {
        const response = await fetch('http://127.0.0.1:8000/api/predict/', {
            method: 'POST',
            body: formData
        });
  
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
  
        const predictions = await response.json();
        displayResults(predictions);
    } catch (error) {
        console.error('Error uploading files:', error);
    }
  });
  
  function displayResults(predictions) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
  
    predictions.forEach(prediction => {
        const img = document.createElement('img');
        img.src = `data:image/png;base64,${prediction.processed_image_base64}`;
        img.alt = prediction.file_name;
  
        const p = document.createElement('p');
        p.textContent = `File: ${prediction.file_name}, Number of boxes: ${prediction.num_boxes}`;
  
        resultsDiv.appendChild(p);
        resultsDiv.appendChild(img);
    });
  }






function reloadPage() {
  location.reload();
}