let menu = document.querySelector('.burger_menu');





const sliderContainer = document.querySelector('.slider-container');
const slider = document.querySelector('.slider');
const slides = Array.from(document.querySelectorAll('.slide'));
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');

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
slider.addEventListener('touchstart', handleTouchStart);
slider.addEventListener('touchmove', handleTouchMove);
slider.addEventListener('touchend', handleTouchEnd);

function handleTouchStart(event) {
  if (isMobile) {
    const touch = event.touches[0];
    let touchStartX = touch.clientX;
  }
}

function handleTouchMove(event) {
  if (isMobile) {
    const touch = event.touches[0];
  }
}

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
window.addEventListener('resize', () => {
  checkScreenSize();
  updateSlideWidth();
});

// Запуск инициализации слайдера при загрузке страницы
initSlider();



















function openburger(){
    let menu = document.querySelector('.burger_menu');
    document.querySelector('.wrapper').style.display='none';


    document.querySelector('.moroj').style.display='none';
    menu.style.display = 'block';
}

function closeburger(){
    let menu = document.querySelector('.burger_menu');
    document.querySelector('.wrapper').style.display='block';


    document.querySelector('.moroj').style.display='block';
    menu.style.display = 'none';
}





function openbuymenu320(){
    let menu = document.querySelector('.burger_menu');
    document.querySelector('.wrapper').style.display='block';
    menu.style.display = 'none';
    document.querySelector('.buy').style.display='block';
    document.querySelector('.first_after_header_section').style.display='none';
    document.querySelector('.second_section').style.display='none';
    document.querySelector('.third_section').style.display='none';
    document.querySelector('.fourth_section').style.display='none';
    document.querySelector('.fifth_section').style.display='none';
    document.querySelector('.button_section').style.display='none';

    document.querySelector('.tochki').style.display='none';
    document.querySelector('.tarelkaMoroj').style.display='none';
    document.querySelector('.moroj').style.display='none';
    
    document.querySelector('.lorem_text').style.display='none'
    document.querySelector('.wrapper967x664').style.height = 'auto'
}

function openbuymenu(){
    document.querySelector('.wrapper967x664').style.height = 'auto'
    document.querySelector('.buy').style.display='block';
    document.querySelector('.first_after_header_section').style.display='none';
    document.querySelector('.second_section').style.display='none';
    document.querySelector('.third_section').style.display='none';
    document.querySelector('.fourth_section').style.display='none';
    document.querySelector('.fifth_section').style.display='none';
    document.querySelector('.button_section').style.display='none';
    document.querySelector('.tochki').style.display='none';
    document.querySelector('.tarelkaMoroj').style.display='none';
    document.querySelector('.moroj').style.display='none';
    document.querySelector('.lorem_text').style.display='none'
}

function gobacktohome(){
    document.querySelector('.buy').style.display='none';
    const screenWidth = window.screen.width; 
    console.log('screenWidth')
    console.log(screenWidth)
    document.querySelector('.first_after_header_section').style.display='flex';
    document.querySelector('.second_section').style.display='block';
    document.querySelector('.third_section').style.display='block';
    document.querySelector('.fourth_section').style.display='block';
    document.querySelector('.fifth_section').style.display='block';
    document.querySelector('.moroj').style.display='block';
    document.querySelector('.button_section').style.display='flex';
    if(screenWidth>=768){
        document.querySelector('.tarelkaMoroj').style.display='block';
        document.querySelector('.lorem_text').style.display='block'
        if(screenWidth==768){
            document.querySelector('.wrapper967x664').style.height = '415px'
        }
        if(screenWidth>=1024){
            document.querySelector('.tochki').style.display='block';
            document.querySelector('.wrapper967x664').style.height = '664px'
            document.querySelector('.tochki').style.display='block';
        }
    }
}

function gobacktohome320(){
    document.querySelector('.buy').style.display='none';
    let menu = document.querySelector('.burger_menu');
    document.querySelector('.wrapper').style.display='block';
    menu.style.display = 'none';
    document.querySelector('.wrapper967x664').style.height = '502px'
    document.querySelector('.first_after_header_section').style.display='flex';
    document.querySelector('.second_section').style.display='block';
    document.querySelector('.third_section').style.display='block';
    document.querySelector('.fourth_section').style.display='block';
    document.querySelector('.fifth_section').style.display='block';
    document.querySelector('.moroj').style.display='block';
    document.querySelector('.button_section').style.display='flex';
    document.querySelector('.moroj').style.display='block';
}


function milkshakes(){
    document.getElementById('1').src = './jpg/milkshake1.jpg'
    document.getElementById('2').src = './jpg/milkshake2.jpeg'
    document.getElementById('3').src = './jpg/milkshake3.jpg'
    document.getElementById('4').src = './jpg/milkshale4.jpg'
    document.getElementById('5').src = './jpg/milkshake5.jpg'
    document.getElementById('6').src = './jpg/milkshake6.jpg'
}

function icecream(){
    document.getElementById('1').src = './png/brooke-lark-8beTH4VkhLI-unsplash 1.png'
    document.getElementById('2').src = './png/courtney-cook-QYsRxRPygwU-unsplash 1.png'
    document.getElementById('3').src = './png/kenta-kikuchi-LZ6BTZnizD8-unsplash 1.png'
    document.getElementById('4').src = './png/image 2.png'
    document.getElementById('5').src = './png/image 3.png'
    document.getElementById('6').src = './png/image 4.png'
}

function icecofee(){
    document.getElementById('1').src = './jpg/icecoffee1.jpeg'
    document.getElementById('2').src = './jpg/icecoffe2.jpg'
    document.getElementById('3').src = './jpg/icecoffee3.jpg'
    document.getElementById('4').src = './jpg/icecoffee4.jpg'
    document.getElementById('5').src = './jpg/icecoffee5.jpg'
    document.getElementById('6').src = './jpg/icecoffee6.jpg'
}

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


function calculate(){

  let quantity = document.querySelector('.Quantity').value
  if(quantity){
    let value = String(price * quantity)
    document.querySelector('.buy_btn_numb').innerHTML = value 
  }
  else{
    alert('Введите количество товара')
  }
  
}



