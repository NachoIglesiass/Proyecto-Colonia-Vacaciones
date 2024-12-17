var swiper = new Swiper('.swiper-container', {
   loop: true, // Desliza de forma continua
   autoplay: {
       delay: 3000, // Intervalo entre imágenes en milisegundos (3 segundos)
       disableOnInteraction: false, // Mantiene autoplay incluso después de interacción del usuario
   },
   pagination: {
       el: '.swiper-pagination',
       clickable: true,
   },
   // navigation: {
   //     nextEl: '.swiper-button-next',
   //     prevEl: '.swiper-button-prev',
   // },
});

// Script para el menú móvil
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const menuLinks = document.querySelectorAll('#mobile-menu a');

menuToggle.addEventListener('click', () => {
    mobileMenu.style.display = mobileMenu.style.display === 'none' ? 'block' : 'none';
});

// Cerrar el menú al hacer clic en un enlace
menuLinks.forEach(link => {
link.addEventListener('click', () => {
     mobileMenu.style.display = 'none'; // Cierra el menú
     const targetId = link.getAttribute('href'); // Obtiene el ID del destino
     const targetElement = document.querySelector(targetId); // Selecciona el elemento destino
     if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' }); // Desplaza suavemente hacia el elemento
        }
});
});