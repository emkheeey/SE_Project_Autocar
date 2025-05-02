// Global variables to track active filters
let activeFilters = {
    bodyType: [],
    price: [],
    transmission: []
};

// Main initialization function - runs when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    // Set up navigation links if they exist
    setupNavigation();
    
    // Set up search functionality
    setupSearch();
    
    // Set up filtering logic
    setupFilters();
    
    // Set up modals
    setupModals();
    
    // Handle profile menu
    setupProfileMenu();
});

// Set up navigation links
function setupNavigation() {
    const homeLink = document.querySelector("a[href='#home']");
    if (homeLink) {
        homeLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/";
        });
    }

    const recommendLink = document.querySelector("a[href='#recommend']");
    if (recommendLink) {
        recommendLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/recommendations/";
        });
    }

    const compareLink = document.querySelector("a[href='#compare-cars']");
    if (compareLink) {
        compareLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/compare/";
        });
    }
    }

// Set up search functionality
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            if (this.value.length > 2) {
                searchCars();
            } else if (this.value.length === 0) {
                showAllCars();
            }
        });
    }
    
    if (searchButton) {
        searchButton.addEventListener('click', searchCars);
    }
}

// Search cars function
function searchCars() {
    const searchInput = document.getElementById("search-input").value.toLowerCase();
    const carCards = document.querySelectorAll(".car-card");

    carCards.forEach(card => {
        const carName = card.querySelector('p').textContent.toLowerCase();
        if (carName.includes(searchInput)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Setup all filter related functionality
function setupFilters() {
    // Setup "All" button
    const allButton = document.getElementById('btn-all');
    if (allButton) {
        allButton.addEventListener('click', function() {
            showAllCars();
            setActiveFilter(this);
        });
    }
    
    // Setup dropdown toggles
    document.querySelectorAll('.filter-btn[data-dropdown]').forEach(btn => {
        btn.addEventListener('click', function() {
            toggleDropdown(this.getAttribute('data-dropdown'));
        });
    });
    
    // Setup body type filters
    document.querySelectorAll('.sub-filter-btn[data-body-type]').forEach(btn => {
        btn.addEventListener('click', function() {
            filterByBodyType(this.getAttribute('data-body-type'));
            setActiveFilter(btn.closest('.dropdown').querySelector('.filter-btn'));
        });
    });
    
    // Setup transmission filters
    document.querySelectorAll('.sub-filter-btn[data-transmission]').forEach(btn => {
        btn.addEventListener('click', function() {
            filterByTransmission(this.getAttribute('data-transmission'));
            setActiveFilter(btn.closest('.dropdown').querySelector('.filter-btn'));
        });
    });
    
    // Setup price filters
    document.querySelectorAll('.sub-filter-btn[data-price-min]').forEach(btn => {
        btn.addEventListener('click', function() {
            const min = parseInt(this.getAttribute('data-price-min'));
            const max = parseInt(this.getAttribute('data-price-max'));
            filterByPrice(min, max);
            setActiveFilter(btn.closest('.dropdown').querySelector('.filter-btn'));
        });
    });
}

// Set up modal functionality
function setupModals() {
    // Setup car details click handlers
    document.querySelectorAll('.car-card').forEach(card => {
        card.addEventListener('click', function() {
            const carId = this.getAttribute('data-car-id');
            const carModel = this.getAttribute('data-model');
            showCarDetails(carId, carModel);
        });
        
        // Prevent image buttons from triggering car details
        const imageBtn = card.querySelector('.update-image-btn');
        if (imageBtn) {
            imageBtn.addEventListener('click', function(event) {
                event.stopPropagation();
                const carId = card.getAttribute('data-car-id');
                const carModel = card.getAttribute('data-model');
                openImageModal(carId, carModel);
            });
        }
    });
    
    // Setup close modal buttons
    const closeImageModalBtn = document.getElementById('closeImageModal');
    if (closeImageModalBtn) {
        closeImageModalBtn.addEventListener('click', closeImageModal);
    }
    
    const closeVariantsModalBtn = document.getElementById('closeVariantsModal');
    if (closeVariantsModalBtn) {
        closeVariantsModalBtn.addEventListener('click', closeModal);
    }
    
    // Setup image form submission
    const imageForm = document.getElementById('imageUrlForm');
    if (imageForm) {
        imageForm.addEventListener('submit', submitImageUrl);
    }
}

// Set up profile menu functionality
function setupProfileMenu() {
    const profileIcon = document.getElementById('profileIcon');
    if (profileIcon) {
        profileIcon.addEventListener('click', toggleMenu);
    }
    
    // Close menu when clicking outside
    window.addEventListener('click', function(event) {
        const menu = document.getElementById('userMenu');
        const icon = document.getElementById('profileIcon');
        
        if (menu && icon && event.target !== icon && !icon.contains(event.target)) {
            menu.style.display = 'none';
        }
        
        // Close modals when clicking outside
        const imageModal = document.getElementById('imageModal');
        if (imageModal && event.target === imageModal) {
            closeImageModal();
        }
        
        const variantsModal = document.getElementById('variantsModal');
        if (variantsModal && event.target === variantsModal) {
            closeModal();
        }
    });
    
    // Close modals with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeImageModal();
            closeModal();
        }
    });
}

// Toggle user menu
function toggleMenu() {
    const menu = document.getElementById("userMenu");
    if (menu) {
    menu.style.display = menu.style.display === "block" ? "none" : "block";
    }
}

// Show all cars and reset filters
function showAllCars() {
    document.querySelectorAll('.car-card').forEach(card => {
        card.style.display = 'block';
    });
    
    // Hide all dropdowns
    document.querySelectorAll('.dropdown-content').forEach(el => {
        el.style.display = 'none';
    });
}

// Helper function to set active filter button
function setActiveFilter(btn) {
    if (!btn) return;
    
    document.querySelectorAll('.filter-btn').forEach(b => {
        b.classList.remove('active');
    });
    
    btn.classList.add('active');
}

// Filter functions
function filterByBodyType(type) {
    document.querySelectorAll('.car-card').forEach(card => {
        card.style.display = card.getAttribute('data-body-type') === type ? 'block' : 'none';
    });
    
    // Hide dropdown after selection
    document.getElementById('bodyTypeDropdown').style.display = 'none';
}

function filterByTransmission(trans) {
    document.querySelectorAll('.car-card').forEach(card => {
        card.style.display = card.getAttribute('data-transmission') === trans ? 'block' : 'none';
    });
    
    // Hide dropdown after selection
    document.getElementById('transmissionDropdown').style.display = 'none';
}

function filterByPrice(min, max) {
    document.querySelectorAll('.car-card').forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        card.style.display = (price >= min && price <= max) ? 'block' : 'none';
    });
    
    // Hide dropdown after selection
    document.getElementById('priceDropdown').style.display = 'none';
}

// Dropdown toggle function
function toggleDropdown(dropdownId) {
    // Hide all dropdowns first
    document.querySelectorAll('.dropdown-content').forEach(el => {
        el.style.display = 'none';
    });
    
    // Toggle the selected dropdown
    const dropdown = document.getElementById(dropdownId);
    if (dropdown) {
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }
}

// Image URL modal functions
function openImageModal(carId, carModel) {
    const modal = document.getElementById('imageModal');
    const title = document.getElementById('imageModalTitle');
    const idInput = document.getElementById('modalCarId');
    const urlInput = document.getElementById('imageUrlInput');
    
    if (modal && title && idInput && urlInput) {
        modal.style.display = 'block';
        title.textContent = `Add/Update Image for ${carModel}`;
        idInput.value = carId;
        urlInput.value = '';
    }
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Car variants modal functions
function showCarDetails(id, model) {
    // TODO: Implement modal or details view
    alert("Show details for " + model + " (ID: " + id + ")");
}

function closeModal() {
    const modal = document.getElementById('variantsModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Form submission for image URL
async function submitImageUrl(event) {
    event.preventDefault();
    const carId = document.getElementById('modalCarId').value;
    const imageUrl = document.getElementById('imageUrlInput').value;
    
    try {
        const response = await fetch(`/accounts/update_car_image/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ car_id: carId, image_url: imageUrl })
        });
        
        if (response.ok) {
            // Update the image in the UI
            const card = document.querySelector(`.car-card[data-car-id='${carId}'] img`);
            if (card) card.src = imageUrl;
            closeImageModal();
            alert('Image updated successfully!');
        } else {
            alert('Failed to update image.');
        }
    } catch (err) {
        alert('Error updating image.');
    }
}

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}