// Get DOM elements
const searchInput = document.getElementById('search-input');
const carList = document.getElementById('car-list');
const searchButton = document.querySelector('.search-button');

// Store original car data
let originalCars = [];
let activeFilters = {
    bodyType: [],
    price: [],
    transmission: []
};

// Initialize when document loads
document.addEventListener('DOMContentLoaded', () => {
    // Store original car cards
    originalCars = Array.from(carList.getElementsByClassName('car-card'));

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

// Show all cars and reset filters
function showAllCars(buttonElement) {
    // Reset active filters
    activeFilters = {
        bodyType: [],
        price: [],
        transmission: []
    };

    // Hide all sub-filter sections
    document.querySelectorAll('.sub-filters').forEach(el => {
        el.style.display = 'none';
    });

    // Remove active class from all buttons
    document.querySelectorAll('.main-filters button, .sub-filters button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to All button
    buttonElement.classList.add('active');

    // Show all cars
    originalCars.forEach(car => {
        car.style.display = 'block';
    });
}

// Show body type filters
function showBodyTypeFilters(buttonElement) {
    // Toggle between showing and hiding
    const bodyTypeFilters = document.getElementById('bodyTypeFilters');
    const isVisible = bodyTypeFilters.style.display !== 'none';

    // Hide all sub-filter sections
    document.querySelectorAll('.sub-filters').forEach(el => {
        el.style.display = 'none';
    });

    // Remove active class from all main filter buttons
    document.querySelectorAll('.main-filters button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to clicked button
    buttonElement.classList.add('active');

    // Show this sub-filter section if it wasn't visible
    if (!isVisible) {
        bodyTypeFilters.style.display = 'flex';
    }

    // Apply any active filters
    applyFilters();
}

// Show price filters
function showPriceFilters(buttonElement) {
    // Toggle between showing and hiding
    const priceFilters = document.getElementById('priceFilters');
    const isVisible = priceFilters.style.display !== 'none';

    // Hide all sub-filter sections
    document.querySelectorAll('.sub-filters').forEach(el => {
        el.style.display = 'none';
    });

    // Remove active class from all main filter buttons
    document.querySelectorAll('.main-filters button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to clicked button
    buttonElement.classList.add('active');

    // Show this sub-filter section if it wasn't visible
    if (!isVisible) {
        priceFilters.style.display = 'flex';
    }

    // Apply any active filters
    applyFilters();
}

// Show transmission filters
function showTransmissionFilters(buttonElement) {
    // Toggle between showing and hiding
    const transmissionFilters = document.getElementById('transmissionFilters');
    const isVisible = transmissionFilters.style.display !== 'none';

    // Hide all sub-filter sections
    document.querySelectorAll('.sub-filters').forEach(el => {
        el.style.display = 'none';
    });

    // Remove active class from all main filter buttons
    document.querySelectorAll('.main-filters button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to clicked button
    buttonElement.classList.add('active');

    // Show this sub-filter section if it wasn't visible
    if (!isVisible) {
        transmissionFilters.style.display = 'flex';
    }

    // Apply any active filters
    applyFilters();
}

// Toggle sub-filter selection
function toggleSubFilter(buttonElement, filterType, filterValue) {
    // Toggle active class
    buttonElement.classList.toggle('active');

    // Update active filters array
    if (buttonElement.classList.contains('active')) {
        // Add filter
        activeFilters[filterType].push(filterValue);
    } else {
        // Remove filter
        const index = activeFilters[filterType].indexOf(filterValue);
        if (index > -1) {
            activeFilters[filterType].splice(index, 1);
        }
    }

    // Apply filters
    applyFilters();
}

// Apply all active filters
function applyFilters() {
    // Check if any filters are active
    const hasActiveFilters = Object.values(activeFilters).some(filters => filters.length > 0);

    if (!hasActiveFilters) {
        // If no filters, show all cars
        originalCars.forEach(car => {
            car.style.display = 'block';
        });
        return;
    }

    // Apply filtering
    originalCars.forEach(carCard => {
        let shouldShow = true;

        // Check body type filters
        if (activeFilters.bodyType.length > 0) {
            const carBodyType = carCard.dataset.type || '';
            if (!activeFilters.bodyType.includes(carBodyType.toLowerCase())) {
                shouldShow = false;
            }
        }

        // Check price filters
        if (shouldShow && activeFilters.price.length > 0) {
            const carPrice = parseInt(carCard.dataset.price || '0');
            let priceMatch = false;

            for (const priceRange of activeFilters.price) {
                if (priceRange === '500000' && carPrice < 500000) {
                    priceMatch = true;
                } else if (priceRange === '1000000' && carPrice >= 500000 && carPrice < 1000000) {
                    priceMatch = true;
                } else if (priceRange === '1500000' && carPrice >= 1000000 && carPrice < 1500000) {
                    priceMatch = true;
                } else if (priceRange === '2000000' && carPrice >= 1500000 && carPrice < 2000000) {
                    priceMatch = true;
                } else if (priceRange === '3000000' && carPrice >= 2000000) {
                    priceMatch = true;
                }
            }

            if (!priceMatch) {
                shouldShow = false;
            }
        }

        // Check transmission filters
        if (shouldShow && activeFilters.transmission.length > 0) {
            const carTransmission = carCard.dataset.transmission || '';
            if (!activeFilters.transmission.includes(carTransmission.toLowerCase())) {
                shouldShow = false;
            }
        }

        // Show or hide based on filter results
        carCard.style.display = shouldShow ? 'block' : 'none';
    });
}

// Function to toggle user menu
function toggleMenu() {
    const userMenu = document.getElementById('userMenu');
    userMenu.style.display = userMenu.style.display === 'block' ? 'none' : 'block';
}

// Function to view car details
function viewCar(carId) {
    window.location.href = `/car/${carId}`;
}

// Logout function
function logout() {
    // Add your logout logic here
    window.location.href = '/accounts/logout/';
}