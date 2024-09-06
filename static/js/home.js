document.addEventListener('DOMContentLoaded', function() {
    console.log('Home page JavaScript loaded.');

    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    console.log('Anchor links:', links);
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            console.log('Target ID:', targetId);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Adjust heights for feature and testimonial cards
    const setEqualHeights = () => {
        const featureCards = document.querySelectorAll('.features .col-md-4');
        const testimonialCards = document.querySelectorAll('.testimonials .testimonial');

        console.log('Feature cards:', featureCards);
        console.log('Testimonial cards:', testimonialCards);

        // Reset heights
        featureCards.forEach(card => card.style.height = 'auto');
        testimonialCards.forEach(card => card.style.height = 'auto');

        const maxFeatureHeight = Math.max(...Array.from(featureCards).map(card => card.offsetHeight));
        const maxTestimonialHeight = Math.max(...Array.from(testimonialCards).map(card => card.offsetHeight));

        console.log('Max feature height:', maxFeatureHeight);
        console.log('Max testimonial height:', maxTestimonialHeight);

        featureCards.forEach(card => card.style.height = `${maxFeatureHeight}px`);
        testimonialCards.forEach(card => card.style.height = `${maxTestimonialHeight}px`);
    };

    // Call the function to adjust heights initially
    setEqualHeights();

    // Re-adjust heights on window resize
    window.addEventListener('resize', setEqualHeights);
});
