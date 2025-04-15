// Sample Data (Replace with actual data from backend/localStorage)
let favorites = [
    { 
        id: 1, 
        model: "Toyota Camry SE", 
        image: "images/cars/camry.jpg",
        price: "₱1,500,000",
        transmission: "Automatic"
    },
    { 
        id: 2, 
        model: "Toyota Hillux", 
        image: "images/cars/hillux.jpg",
        price: "₱1,800,000",
        transmission: "Manual" 
    },
    { 
        id: 3, 
        model: "Toyota Fortuner", 
        image: "images/cars/fortuner.jpg",
        price: "₱2,200,000",
        transmission: "Automatic" 
    }
];

// DOM Elements
const favoritesGrid = document.getElementById('favoritesGrid');
const emptyState = document.getElementById('emptyState');
const compareBtn = document.getElementById('compareBtn');
const compareModal = document.getElementById('compareModal');
const compareCheckboxes = document.getElementById('compareCheckboxes');

// Initialize Page
document.addEventListener('DOMContentLoaded', function() {
    renderFavorites();
    updateUI();
});

// Render Favorites List
function renderFavorites() {
    favoritesGrid.innerHTML = '';
    
    favorites.forEach(car => {
        const card = document.createElement('div');
        card.className = 'favorite-card';
        card.innerHTML = `
            <img src="${car.image}" alt="${car.model}">
            <div class="card-content">
                <h3>${car.model}</h3>
                <p>${car.price} • ${car.transmission}</p>
            </div>
            <button class="remove-btn" onclick="removeFavorite(${car.id})">
                <i class="fas fa-times"></i>
            </button>
        `;
        card.addEventListener('click', () => viewCarDetails(car.id));
        favoritesGrid.appendChild(card);
    });
}

// Update UI Based on Favorites
function updateUI() {
    if (favorites.length === 0) {
        emptyState.classList.remove('hidden');
        favoritesGrid.classList.add('hidden');
        compareBtn.classList.add('hidden');
    } else {
        emptyState.classList.add('hidden');
        favoritesGrid.classList.remove('hidden');
        compareBtn.classList.remove('hidden');
    }
}

// Remove Favorite
function removeFavorite(carId) {
    event.stopPropagation(); // Prevent card click event
    if (confirm('Remove this car from favorites?')) {
        favorites = favorites.filter(car => car.id !== carId);
        renderFavorites();
        updateUI();
        // Update backend/localStorage here
    }
}

// View Car Details
function viewCarDetails(carId) {
    window.location.href = `car-details.html?id=${carId}`;
}

// Compare Modal Functions
function openCompareModal() {
    compareCheckboxes.innerHTML = '';
    
    favorites.forEach((car, index) => {
        const item = document.createElement('div');
        item.className = 'checkbox-item';
        item.innerHTML = `
            <input type="checkbox" id="car-${car.id}" value="${car.id}">
            <img src="${car.image}" alt="${car.model}">
            <label for="car-${car.id}">${car.model}</label>
        `;
        compareCheckboxes.appendChild(item);
    });
    
    compareModal.classList.remove('hidden');
}

function closeCompareModal() {
    compareModal.classList.add('hidden');
}

function proceedToCompare() {
    const selectedCars = [];
    document.querySelectorAll('#compareCheckboxes input:checked').forEach(checkbox => {
        selectedCars.push(checkbox.value);
    });
    
    if (selectedCars.length < 2 || selectedCars.length > 3) {
        alert('Please select 2 or 3 cars to compare');
        return;
    }
    
    // Store selected cars and redirect
    localStorage.setItem('compareCars', JSON.stringify(selectedCars));
    window.location.href = `compare.html?from=favorites`;
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    if (event.target === compareModal) {
        closeCompareModal();
    }
});