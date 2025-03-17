document.addEventListener('DOMContentLoaded', function () {
    const carImages = ['camry1.png', 'camry2.png', 'camry3.png', 'camry4.png'];
    let currentIndex = 0;
    const carImageElement = document.getElementById('car-image');

    // Navigation Buttons
    document.getElementById('prev-btn').addEventListener('click', function () {
        currentIndex = (currentIndex === 0) ? carImages.length - 1 : currentIndex - 1;
        carImageElement.src = `images/cars/${carImages[currentIndex]}`;
    });

    document.getElementById('next-btn').addEventListener('click', function () {
        currentIndex = (currentIndex === carImages.length - 1) ? 0 : currentIndex + 1;
        carImageElement.src = `images/cars/${carImages[currentIndex]}`;
    });

    // Favorite Button
    document.getElementById('favorite-btn').addEventListener('click', function () {
        alert('Added to favorites!');
        // Add logic to save to local storage or database
    });
});

