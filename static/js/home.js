document.addEventListener('DOMContentLoaded', function() {
  console.log('Home page JavaScript loaded.');

  // Smooth scrolling for anchor links
  const links = document.querySelectorAll('a[href^="#"]');
  console.log('Anchor links found:', links);
  links.forEach(link => {
      link.addEventListener('click', function(event) {
          event.preventDefault();
          const targetId = this.getAttribute('href').substring(1);
          console.log('Target ID:', targetId);
          const targetElement = document.getElementById(targetId);
          if (targetElement) {
              console.log('Scrolling to element:', targetElement);
              targetElement.scrollIntoView({
                  behavior: 'smooth'
              });
          } else {
              console.warn('Target element not found:', targetId);
          }
      });
  });
});
