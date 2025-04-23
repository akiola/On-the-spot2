/**
 * On the Spot Transfer - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
            const icon = mobileMenuToggle.querySelector('i');
            if (navMenu.classList.contains('show')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
    
    // Close flash messages
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // Testimonial slider auto-scroll
    const testimonialSlider = document.querySelector('.testimonial-slider');
    if (testimonialSlider) {
        let scrollAmount = 0;
        const scrollSpeed = 2;
        const testimonialWidth = testimonialSlider.querySelector('.testimonial').offsetWidth + 30; // 30 is the gap
        const maxScroll = testimonialSlider.scrollWidth - testimonialSlider.clientWidth;
        let direction = 1; // 1 for right, -1 for left
        
        function autoScroll() {
            if (scrollAmount >= maxScroll) {
                direction = -1;
            } else if (scrollAmount <= 0) {
                direction = 1;
            }
            
            scrollAmount += (scrollSpeed * direction);
            testimonialSlider.scrollLeft = scrollAmount;
            
            // Only continue auto-scrolling if user isn't hovering
            if (!testimonialSlider.matches(':hover')) {
                requestAnimationFrame(autoScroll);
            }
        }
        
        // Start auto-scrolling
        setTimeout(() => {
            requestAnimationFrame(autoScroll);
        }, 3000);
        
        // Pause auto-scrolling on hover
        testimonialSlider.addEventListener('mouseenter', function() {
            // Auto-scroll is paused because of the hover check in autoScroll
        });
        
        // Resume auto-scrolling when hover ends
        testimonialSlider.addEventListener('mouseleave', function() {
            requestAnimationFrame(autoScroll);
        });
        
        // Handle manual scrolling
        testimonialSlider.addEventListener('scroll', function() {
            scrollAmount = testimonialSlider.scrollLeft;
        });
    }
    
    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close all FAQ items
                faqItems.forEach(faqItem => {
                    faqItem.classList.remove('active');
                });
                
                // Open the clicked item if it wasn't active before
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });
    
    // Animated counter for numbers
    function animateCounter(element, target, duration) {
        let start = 0;
        const increment = target / (duration / 16); // 16ms is roughly 60fps
        
        function updateCount() {
            start += increment;
            element.textContent = Math.floor(start);
            
            if (start < target) {
                requestAnimationFrame(updateCount);
            } else {
                element.textContent = target;
            }
        }
        
        updateCount();
    }
    
    // Animate counters when they come into view
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-target'));
                    animateCounter(entry.target, target, 1500);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
    }
    
    // Current year for footer
    const yearElements = document.querySelectorAll('.current-year');
    yearElements.forEach(el => {
        el.textContent = new Date().getFullYear();
    });
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]:not([href="#"])');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // 80px offset for header
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Add error message if it doesn't exist
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('error-message')) {
                        const errorMessage = document.createElement('div');
                        errorMessage.classList.add('error-message');
                        errorMessage.textContent = 'This field is required';
                        field.parentElement.insertBefore(errorMessage, field.nextElementSibling);
                    }
                } else {
                    field.classList.remove('error');
                    
                    // Remove error message if it exists
                    if (field.nextElementSibling && field.nextElementSibling.classList.contains('error-message')) {
                        field.nextElementSibling.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
});