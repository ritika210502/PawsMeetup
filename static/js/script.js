$(document).ready(function() {
    // Navigation Toggle
    $('.navbar-toggler').click(function(){
        $('.navbar-collapse').toggleClass('show');
    });

    // Form Validation for Registration Form
    $('#register-form').on('submit', function(event) {
        var password = $('#id_password1').val();
        var confirmPassword = $('#id_password2').val();
        
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            event.preventDefault();  // Prevent form submission
        }
    });

    // Smooth Scrolling for Anchor Links
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        var target = this.hash;
        $('html, body').stop().animate({
            'scrollTop': $(target).offset().top
        }, 300, 'swing', function() {
            window.location.hash = target;
        });
    });

    // Basic Carousel
    $('.carousel').carousel({
        interval: 5000  // 5 seconds
    });

    // Dynamic Content Loading for Dog List Filtering
    $('#size').on('change', function(){
        var selectedSize = $(this).val();
        $.ajax({
            url: "{% url 'dog_list' %}",  // Make sure this URL is correctly set up
            data: { size: selectedSize },
            success: function(response) {
                $('#dog-list').html(response);  // Update content dynamically
            }
        });
    });

    // Toggle Alerts
    $('.alert').fadeIn().delay(3000).fadeOut();

    // Expand/Collapse Content for FAQs
    $('.faq-question').click(function(){
        $(this).next('.faq-answer').slideToggle();
        $(this).toggleClass('active');
    });

    // Custom Animation for Elements Coming into View
    $(window).on('scroll', function() {
        $('.animate-on-scroll').each(function(){
            if ($(this).offset().top < $(window).scrollTop() + $(window).height() - 50) {
                $(this).addClass('fade-in');
            }
        });
    });
});
