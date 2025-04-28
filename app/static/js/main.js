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