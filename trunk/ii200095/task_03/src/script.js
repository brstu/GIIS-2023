const slides = Array.from(document.querySelectorAll(".slide"));
const prevButton = document.querySelector(".prev-button");
const nextButton = document.querySelector(".next-button");

let slideWidth = slides[0].offsetWidth;
let currentIndex = 0;
let isMobile = false;

// Проверка разрешения экрана
function checkScreenSize() {
  isMobile = window.innerWidth <= 320;
}

// Обновление ширины слайдов при изменении размера экрана
function updateSlideWidth() {
  slideWidth = slides[0].offsetWidth;
  slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}

// Функция для переключения на предыдущий слайд
function goToPrevSlide() {
  if (currentIndex > 0) {
    currentIndex--;
    slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
  }
}

// Функция для переключения на следующий слайд
function goToNextSlide() {
  if (currentIndex < slides.length - 1) {
    currentIndex++;
    slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
  }
}

prevButton.addEventListener('click', goToPrevSlide);
nextButton.addEventListener('click', goToNextSlide);

// Обработка событий для мобильных устройств
slider.addEventListener('touchend', handleTouchEnd);

function handleTouchEnd() {
  if (isMobile) {
    const diffX = touchStartX - touchMoveX;
    const threshold = slideWidth / 4;

    if (diffX > threshold) {
      goToNextSlide();
    } else if (diffX < -threshold) {
      goToPrevSlide();
    }
  }
}

// Инициализация слайдера
function initSlider() {
  checkScreenSize();
  updateSlideWidth();
}

// Обработка изменения размера экрана
window.addEventListener("resize", () => {
  checkScreenSize();
  updateSlideWidth();
});

// Запуск инициализации слайдера при загрузке страницы
initSlider();

const prices = [3,5,7]
let price = prices[0]

document.querySelector('.choise1').addEventListener('click',()=>{
  price = prices[0]
  document.querySelector('.choise2').style.background = '#fff'
  document.querySelector('.choise3').style.background = '#fff'
  document.querySelector('.choise1').style.background = '#96AF8C'
})

document.querySelector('.choise2').addEventListener('click',()=>{
  price = prices[1]
  document.querySelector('.choise2').style.background = '#EFD478'
  document.querySelector('.choise3').style.background = '#fff'
  document.querySelector('.choise1').style.background = '#fff'
})

document.querySelector('.choise3').addEventListener('click',()=>{
  price = prices[2]
  document.querySelector('.choise2').style.background = '#fff'
  document.querySelector('.choise3').style.background = '#D6936D'
  document.querySelector('.choise1').style.background = '#fff'
})
