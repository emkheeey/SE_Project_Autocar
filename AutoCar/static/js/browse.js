// Get DOM elements
const searchInput = document.getElementById('search-input');
const carList = document.getElementById('car-list');
const filterBoxes = document.querySelectorAll('.filter-box');
const searchButton = document.querySelector('.search-button'); // Add this line

// Store original car data
let originalCars = [];

// Initialize when document loads
document.addEventListener('DOMContentLoaded', () => {
    // Store original car cards
    originalCars = Array.from(carList.getElementsByClassName('car-card'));

    // Remove real-time search
    // searchInput.removeEventListener('input', handleSearch);

    // Add search button click event
    searchButton.addEventListener('click', function () {
        const searchTerm = searchInput.value.toLowerCase().trim();
        performSearch(searchTerm);
    });

    // Add enter key support
    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            const searchTerm = searchInput.value.toLowerCase().trim();
            performSearch(searchTerm);
        }
    });

    // Add click events to filter boxes
    filterBoxes.forEach(box => {
        box.addEventListener('click', () => handleFilter(box.textContent));
    });
});

// New separate search function
function performSearch(searchTerm) {
    if (searchTerm === '') {
        // If search is empty, show all cars
        originalCars.forEach(car => car.style.display = 'block');
    } else {
        // Hide all cars first
        originalCars.forEach(car => car.style.display = 'none');

        // Show only matching cars
        originalCars.forEach(carCard => {
            const carName = carCard.querySelector('p').textContent.toLowerCase();
            if (carName.includes(searchTerm)) {
                carCard.style.display = 'block';
            }
        });
    }
}

// Filter functionality (unchanged)
function handleFilter(filterType) {
    // Remove active class from all filter boxes
    filterBoxes.forEach(box => box.classList.remove('active'));

    // Add active class to selected filter
    const selectedFilter = Array.from(filterBoxes).find(box => box.textContent === filterType);
    selectedFilter.classList.add('active');

    // Show all cars if 'All' is selected
    if (filterType === 'All') {
        originalCars.forEach(car => car.style.display = 'block');
        return;
    }

    // Apply filter based on type
    originalCars.forEach(carCard => {
        const carType = carCard.dataset.type;
        if (carType === filterType.toLowerCase()) {
            carCard.style.display = 'block';
        } else {
            carCard.style.display = 'none';
        }
    });
}