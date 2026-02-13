/**
 * Main JavaScript file for Expense Tracker
 * Handles client-side interactions and enhancements
 */

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Slide out animation for flash messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation enhancement
const forms = document.querySelectorAll('.expense-form');
forms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const amount = form.querySelector('[name="amount"]');
        const category = form.querySelector('[name="category"]');
        const date = form.querySelector('[name="date"]');
        
        let isValid = true;
        let errorMessage = '';
        
        // Validate amount
        if (amount && (parseFloat(amount.value) <= 0 || isNaN(amount.value))) {
            isValid = false;
            errorMessage = 'Please enter a valid amount greater than 0';
        }
        
        // Validate category
        if (category && !category.value) {
            isValid = false;
            errorMessage = 'Please select a category';
        }
        
        // Validate date
        if (date && !date.value) {
            isValid = false;
            errorMessage = 'Please select a date';
        }
        
        if (!isValid) {
            e.preventDefault();
            alert(errorMessage);
        }
    });
});

// Confirmation for delete actions
const deleteForms = document.querySelectorAll('form[action*="delete"]');
deleteForms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const confirmed = confirm('Are you sure you want to delete this expense?');
        if (!confirmed) {
            e.preventDefault();
        }
    });
});

// Add loading indicator for forms
forms.forEach(function(form) {
    form.addEventListener('submit', function() {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Saving...';
        }
    });
});

// Helper function to format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Helper function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Export functions for use in other scripts
window.ExpenseTracker = {
    formatCurrency: formatCurrency,
    formatDate: formatDate
};

// Log application ready
console.log('Expense Tracker initialized successfully!');
