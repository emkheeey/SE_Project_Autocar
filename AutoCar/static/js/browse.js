// Simple debug script
console.log('browse.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded');
    
    // Log how many car cards we have
    const carCards = document.querySelectorAll('.car-card');
    console.log('Found ' + carCards.length + ' car cards');
    
    // Add click handlers to car cards
    carCards.forEach(card => {
        card.addEventListener('click', function() {
            const carId = this.getAttribute('data-car-id');
            console.log('Car clicked: ' + carId);
            alert('You clicked on car ID: ' + carId);
        });
    });
});