import './style.css'

function scrollDown() {
  window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
  });
}


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


