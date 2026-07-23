
const menuToggle = document.querySelector(".menu-toggle");
const nav = document.querySelector("nav");

console.log(menuToggle);

menuToggle.addEventListener("click", function() {
    nav.classList.toggle("active");
    menuToggle.classList.toggle("open");

    if (menuToggle.classList.contains("open")) {
        menuToggle.innerHTML = "✕";
    } else {
        menuToggle.innerHTML = "☰";
    }
});

const navLinks = document.querySelectorAll("nav a");

navLinks.forEach(function(link) {
    link.addEventListener("click", function() {
        nav.classList.remove("active");
        menuToggle.classList.remove("open");
        menuToggle.innerHTML = "☰";
    });
});