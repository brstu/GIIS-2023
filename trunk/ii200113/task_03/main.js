const navbar = document.querySelector("#navbart")
const div = document.querySelector(".none")

navbar.addEventListener('click', () => {
    div.classList.toggle('active');
  });