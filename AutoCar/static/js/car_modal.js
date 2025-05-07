// This script handles car modals
document.addEventListener('DOMContentLoaded', function() {
    console.log('car_modal.js loaded - DEBUG MODE');
    console.log('Document ready state:', document.readyState);
    
    // Direct approach - add onclick handlers to all car cards
    console.log('Adding direct onclick handlers...');
    const carCards = document.querySelectorAll('.car-card');
    console.log('Found ' + carCards.length + ' car cards');
    
    if (carCards.length > 0) {
        carCards.forEach(card => {
            const carId = card.getAttribute('data-car-id');
            console.log('Setting up direct handler for card ID:', carId);
            
            // Use onclick property directly
            card.onclick = function(e) {
                e.preventDefault(); // Prevent any default action
                e.stopPropagation(); // Stop event bubbling
                console.log('Car card clicked with ID:', carId);
                openCarModal(carId);
                return false; // Extra prevention of default behavior
            };
            
            // Also make the "View Details" button work
            const viewButton = card.querySelector('.car-link');
            if (viewButton) {
                viewButton.onclick = function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('View Details button clicked for car ID:', carId);
                    openCarModal(carId);
                    return false;
                };
            }
        });
    } else {
        console.error('No car cards found on page!');
    }
    
    // Setup modal closing
    console.log('Setting up modal close handlers...');
    setupModalClose();
});

function setupModalClose() {
    // Close modal when X is clicked
    const closeButton = document.querySelector('.modal-close');
    if (closeButton) {
        closeButton.onclick = function(e) {
            e.preventDefault();
            closeCarModal();
            return false;
        };
    }
    
    // Close modal when clicking outside
    const modal = document.getElementById('carModal');
    if (modal) {
        modal.onclick = function(e) {
            if (e.target === this) {
                closeCarModal();
            }
        };
    }
    
    // Close with escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeCarModal();
        }
    });
}

function openCarModal(carId) {
    console.log('Opening modal for car ID:', carId);
    
    // Convert carId to a number if it's a string
    carId = parseInt(carId);
    
    // Find the car in our data array (defined in the template)
    const car = window.carsData.find(c => c.id === carId);
    if (!car) {
        console.error('Car data not found for ID:', carId);
        return;
    }
    
    // Update modal with car details
    document.getElementById('modalCarTitle').textContent = car.model;
    document.getElementById('modalCarYear').textContent = car.year;
    document.getElementById('modalCarPrice').textContent = '₱' + car.price;
    document.getElementById('modalCarBodyType').textContent = car.body_type;
    document.getElementById('modalCarTransmission').textContent = car.transmission;
    document.getElementById('modalCarFuelType').textContent = car.fuel_type;
    document.getElementById('modalCarSeats').textContent = car.num_seats;
    document.getElementById('modalCarOutput').textContent = car.max_output;
    document.getElementById('modalCarDrivetrain').textContent = car.drivetrain;
    
    // Set the image
    const modalImage = document.getElementById('modalCarImage');
    if (car.image_url && car.image_url !== 'none') {
        modalImage.src = car.image_url;
        modalImage.style.display = 'block';
    } else {
        modalImage.style.display = 'none';
    }
    
    // Fetch variants for this car
    fetchCarVariants(carId);
    
    // Show the modal
    const modal = document.getElementById('carModal');
    modal.style.display = 'flex';
    
    // Prevent scrolling on the body
    document.body.style.overflow = 'hidden';
}

function closeCarModal() {
    console.log('Closing car modal');
    const modal = document.getElementById('carModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

function fetchCarVariants(carId) {
    const variantsSection = document.getElementById('modalVariantsSection');
    const variantsList = document.getElementById('modalVariantsList');
    
    if (!variantsList) {
        console.error('Variants list element not found');
        return;
    }
    
    // Clear previous variants
    variantsList.innerHTML = '<p>Loading variants...</p>';
    
    // Fetch variants using fetch API with correct URL path
    fetch(`/accounts/cars/variants-json/${carId}/`)
        .then(response => {
            console.log('Variants API response:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Variants data received:', data);
            if (data.variants && data.variants.length > 0) {
                // Show variants section
                if (variantsSection) {
                    variantsSection.style.display = 'block';
                }
                
                // Build variants list
                let variantsHtml = '';
                data.variants.forEach(variant => {
                    variantsHtml += `
                        <div class="variant-card">
                            <h3>${variant.model}</h3>
                            <p class="price">₱${variant.price}</p>
                            <div class="specs">
                                <p><strong>Engine:</strong> ${variant.max_output || 'N/A'}</p>
                                <p><strong>Transmission:</strong> ${variant.transmission || 'N/A'}</p>
                                <p><strong>Fuel Type:</strong> ${variant.fuel_type || 'N/A'}</p>
                            </div>
                        </div>
                    `;
                });
                
                variantsList.innerHTML = variantsHtml;
            } else {
                // No variants found
                variantsList.innerHTML = '<p>No variants available for this model.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching variants:', error);
            variantsList.innerHTML = `
                <p>Failed to load variants: ${error.message}</p>
                <p>Using direct URL may work better: 
                   <a href="/accounts/cars/${carId}/" target="_blank">View Detail Page</a>
                </p>
            `;
        });
} 