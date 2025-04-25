// Toggle user menu
function toggleMenu() {
    const menu = document.getElementById('userMenu');
    menu.classList.toggle('active');
}

// Close menu when clicking outside
document.addEventListener('click', function (event) {
    const menu = document.getElementById('userMenu');
    const profileIcon = document.querySelector('.profile-icon');

    if (menu && profileIcon) {
        if (!menu.contains(event.target) && !profileIcon.contains(event.target)) {
            menu.classList.remove('active');
        }
    }
});

// Logout function
function logout() {
    // Create a form to submit the POST request
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/accounts/logout/';

    // Add CSRF token from the cookie
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;

    form.appendChild(csrfInput);
    document.body.appendChild(form);
    form.submit();
}