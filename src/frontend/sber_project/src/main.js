import './style.css'

function scrollDown() {
  window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
  });
}


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

