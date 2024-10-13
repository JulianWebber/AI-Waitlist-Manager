document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('waitlist-form');
    const successMessage = document.getElementById('success-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const fullName = document.getElementById('full-name').value;
        const email = document.getElementById('email').value;

        // Basic form validation
        if (!fullName || !email) {
            alert('Please fill in all fields');
            return;
        }

        if (!isValidEmail(email)) {
            alert('Please enter a valid email address');
            return;
        }

        // Send data to server
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ full_name: fullName, email: email }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                form.reset();
                successMessage.style.display = 'block';
                successMessage.textContent = data.message;
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 5000);
            } else {
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});
