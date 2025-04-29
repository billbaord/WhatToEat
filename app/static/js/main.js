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
    const loginForm = document.querySelector('.auth-form form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.querySelector('#username');
            const password = document.querySelector('#password');
            
            if (!username.value.trim()) {
                e.preventDefault();
                alert('Please enter your username');
                username.focus();
                return false;
            }
            
            if (!password.value) {
                e.preventDefault();
                alert('Please enter your password');
                password.focus();
                return false;
            }
        });
    }
    document.addEventListener('DOMContentLoaded', function() {
        // Add form validation for recipe form
        const recipeForm = document.querySelector('#recipe-form');
        if (recipeForm) {
            recipeForm.addEventListener('submit', function(e) {
                const title = document.querySelector('#title');
                const description = document.querySelector('#description');
                const ingredients = document.querySelector('#ingredients');
                const instructions = document.querySelector('#instructions');
                
                if (!title.value.trim()) {
                    e.preventDefault();
                    alert('Please enter a title');
                    title.focus();
                    return false;
                }
                
                if (!description.value.trim()) {
                    e.preventDefault();
                    alert('Please enter a description');
                    description.focus();
                    return false;
                }
                
                if (!ingredients.value.trim()) {
                    e.preventDefault();
                    alert('Please enter ingredients');
                    ingredients.focus();
                    return false;
                }
                
                if (!instructions.value.trim()) {
                    e.preventDefault();
                    alert('Please enter instructions');
                    instructions.focus();
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
})