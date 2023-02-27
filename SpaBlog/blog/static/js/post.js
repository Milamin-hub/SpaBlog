// Получаем элементы изображений и текстовых файлов
const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
const textInputs = document.querySelectorAll('input[type="file"][accept="text/plain"]');

// Функция для изменения размера изображения
function resizeImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      let width = img.width;
      let height = img.height;
      if (width > 320 || height > 240) {
        if (width > height) {
          height *= 320 / width;
          width = 320;
        } else {
          width *= 240 / height;
          height = 240;
        }
      }
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);
      canvas.toBlob(resolve, 'image/jpeg', 0.9);
    };
    img.onerror = reject;
    img.src = URL.createObjectURL(file);
  });
}

// Функция для проверки размера текстового файла
function checkTextSize(file) {
  return new Promise((resolve, reject) => {
    if (file.size > 100000) {
      reject('File size exceeds 100KB');
    } else {
      resolve();
    }
  });
}

// Обработчик события для изменения размера изображения и проверки размера текстового файла
function handleInputChange(event) {
  const input = event.target;
  const files = input.files;
  const isImage = input.accept === 'image/*';
  const promises = [];
  for (const file of files) {
    if (isImage) {
      promises.push(resizeImage(file));
    } else {
      promises.push(checkTextSize(file));
    }
  }
  Promise.all(promises)
    .then(() => {
      // Визуальные эффекты для просмотра файлов
      // Например, можно использовать библиотеку Lightbox2
    })
    .catch(error => {
      alert(error);
      input.value = '';
    });
}

// Добавляем обработчик события для каждого элемента изображения и текстового файла
for (const input of imageInputs) {
  input.addEventListener('change', handleInputChange);
}
for (const input of textInputs) {
  input.addEventListener('change', handleInputChange);
}