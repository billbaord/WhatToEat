// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.delete-recipe');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this recipe?')) {
                e.preventDefault();
            }
        });
    });
    // Registration Page
    const registerForm = document.querySelector('.auth-form form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const username = document.querySelector('#username');
            const email = document.querySelector('#email');
            const password = document.querySelector('#password');
            const password_repeat = document.querySelector('#password_repeat');
            
            let isValid = true;
            
            if (!username.value.trim()) {
                e.preventDefault();
                alert('Please enter a username');
                username.focus();
                return false;
            }
            
            if (!email.value.trim()) {
                e.preventDefault();
                alert('Please enter an email');
                email.focus();
                return false;
            }
            
            if (!password.value) {
                e.preventDefault();
                alert('Please enter a password');
                password.focus();
                return false;
            }
            
            if (!password_repeat.value) {
                e.preventDefault();
                alert('Please confirm your password');
                password_repeat.focus();
                return false;
            }
            
            if (password.value !== password_repeat.value) {
                e.preventDefault();
                alert('Passwords do not match');
                return false;
            }
        });
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

