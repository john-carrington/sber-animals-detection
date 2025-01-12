const carousel = document.getElementById('carousel');
const leftArrow = document.querySelector(".left-arrow");
const rightArrow = document.querySelector(".right-arrow");
const modal = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const closeBtn = document.querySelector('.close');

let currentIndex = 0;
let images;
let totalImages;
const imageWidth = 300;
const carouselWidth = 900;

leftArrow.addEventListener("click", () => {
    if (currentIndex > 0 && totalImages > 4) {
        currentIndex--;
        updateCarousel();
    };
});

rightArrow.addEventListener("click", () => {
    if (currentIndex < totalImages - 1 && totalImages > 4) {
        currentIndex++;
        updateCarousel();
    }
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
        alert('Соединение устанавливается, пожалуйста подождите ответа');
        const response = await fetch('http://127.0.0.1:8000/api/predict/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const predictions = await response.json();
        // Сохраняем результаты в localStorage
        localStorage.setItem('predictions', JSON.stringify(predictions));
        alert('Файлы успешно загружены и обработаны. Нажмите "Перейти к анализу снимков" для просмотра результатов.');
        
    } catch (error) {
        console.error('Error uploading files:', error);
        alert('Ошибка при загрузке файлов. Пожалуйста, попробуйте еще раз.');
    }
});

document.getElementById('activeButton').addEventListener('click', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение кнопки
    reloadPage();
    fillTableWithPredictions(predictions);
});

function reloadPage() {
    location.reload();
}

function displayResults() {
    const resultsDiv = document.getElementById('carousel');
    resultsDiv.innerHTML = ''; // Очищаем предыдущие результаты

    const predictions = JSON.parse(localStorage.getItem('predictions'));
    if (predictions) {
        predictions.forEach(prediction => {
            const img = document.createElement('img');
            img.src = `data:image/png;base64,${prediction.processed_image_base64}`;
            img.className = 'carousel-image';
            img.style.maxWidth = `${imageWidth}px`;
            img.addEventListener('click', function() {
                modal.style.display = 'block';
                modalImg.src = this.src;
            });
            resultsDiv.appendChild(img);
        });

        images = document.querySelectorAll(".carousel-image");
        totalImages = images.length;

        // Инициализируем карусель
        updateCarousel();

        // Заполняем таблицу данными
        fillTableWithPredictions(predictions);
    } else {
        resultsDiv.innerHTML = '<p>Нет результатов для отображения.</p>';
    }
}

function updateCarousel() {
    const offset = currentIndex * (imageWidth + 20);
    if (currentIndex === 0) {
        carousel.style.transform = `translateX(${300}px)`;
    } else {
        carousel.style.transform = `translateX(-${offset/2}px)`;
    }
    carousel.classList.add("sliding-transition");

    setTimeout(() => {
        carousel.classList.remove("sliding-transition");
    }, 490);

    // Проверка, нужно ли блокировать кнопки:
    // Отключаем кнопки в зависимости от положения карусели
    leftArrow.disabled = currentIndex === (0 - totalImages); // Блокируем кнопку слева на первом изображении
    rightArrow.disabled = currentIndex === Math.floor(totalImages / 2); // Блокируем кнопку справа на последнем изображении
}

window.onload = displayResults;

function fillTableWithPredictions(predictions) {
    // Получаем tbody таблицы
    const tbody = document.querySelector("tbody");

    // Очищаем таблицу перед добавлением новых данных
    tbody.innerHTML = '';

    // Проходим по каждому элементу в predictions и добавляем строки в таблицу
    predictions.forEach(prediction => {
        const row = document.createElement('tr');

        // Создаем ячейку для названия
        const nameCell = document.createElement('td');
        nameCell.textContent = prediction.file_name;
        row.appendChild(nameCell);

        // Создаем ячейку для num_boxes
        const numBoxesCell = document.createElement('td');
        numBoxesCell.className = "metric_count";  // Присваиваем класс для стилизации
        numBoxesCell.textContent = prediction.num_boxes;
        row.appendChild(numBoxesCell);

        // Добавляем строку в tbody
        tbody.appendChild(row);
    });
}
