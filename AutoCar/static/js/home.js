document.addEventListener('DOMContentLoaded', function() {
    // Get the compare button
    const compareButton = document.querySelector('.comparebtn');
    
    // Add click event listener to the compare button
    if (compareButton) {
        compareButton.addEventListener('click', function() {
            // Redirect to the favorites page where cars can be compared
            window.location.href = '/accounts/favorites/';
        });
    }
}); 