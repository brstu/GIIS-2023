let isDay = true;

// Изменение фона каждые 3 секунды
function toggleWeather() {
  const body = document.querySelector('body');

  if (isDay) {
    body.classList.add('night');
    isDay = false;
  } else {
    body.classList.remove('night');
    isDay = true;
  }
}

setInterval(() => {
  toggleWeather();
}, 3000);
