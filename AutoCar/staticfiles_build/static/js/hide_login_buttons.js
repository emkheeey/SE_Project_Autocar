// Hide login buttons script
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in (presence of certain elements can indicate this)
    const userIsLoggedIn = document.querySelector('.user-menu') !== null;
    
    // Get login/register buttons if they exist
    const loginButtons = document.querySelectorAll('.login-button, .register-button');
    
    // Hide login buttons if user is logged in
    if (userIsLoggedIn) {
        loginButtons.forEach(function(button) {
            button.style.display = 'none';
        });
    }
    
    console.log('Hide login buttons script loaded successfully');
});
