document.addEventListener('DOMContentLoaded', function() {
    // User dropdown functionality
    const userToggle = document.getElementById('userToggle');
    const userDropdown = document.getElementById('userDropdown');
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarMenu = document.getElementById('navbarMenu');

    // Toggle user dropdown
    if (userToggle && userDropdown) {
        userToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');

            // Close mobile menu if open
            if (navbarMenu) {
                navbarMenu.classList.remove('show');
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userToggle.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // Mobile menu toggle
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navbarMenu.classList.toggle('show');

            // Close user dropdown if open
            if (userDropdown) {
                userDropdown.classList.remove('show');
            }

            // Toggle hamburger animation
            navbarToggle.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarToggle.contains(e.target) && !navbarMenu.contains(e.target)) {
                navbarMenu.classList.remove('show');
                navbarToggle.classList.remove('active');
            }
        });
    }

    // Alert dismissal
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Close dropdowns on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // Close user dropdown
            if (userDropdown) {
                userDropdown.classList.remove('show');
            }
            // Close mobile menu
            if (navbarMenu) {
                navbarMenu.classList.remove('show');
            }
            if (navbarToggle) {
                navbarToggle.classList.remove('active');
            }
        }
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="icon-loader"></i> Processing...';
            }
        });
    });

});
