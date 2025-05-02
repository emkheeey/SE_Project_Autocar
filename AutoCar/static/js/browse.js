// Global variables to track active filters
let activeFilters = {
    bodyType: [],
    price: [],
    transmission: []
};

// Navigation handlers
document.addEventListener("DOMContentLoaded", function () {
    // Set up navigation links if they exist
    const homeLink = document.querySelector("a[href='#home']");
    if (homeLink) {
        homeLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/";  // Update with your home URL
        });
    }

    const recommendLink = document.querySelector("a[href='#recommend']");
    if (recommendLink) {
        recommendLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/recommendations/";  // Update with your recommendations URL
        });
    }

    const compareLink = document.querySelector("a[href='#compare-cars']");
    if (compareLink) {
        compareLink.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "/compare/";  // Update with your compare URL
        });
    }

    // Add input event to search for instant results
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            if (this.value.length > 2) {  // Only search if at least 3 characters
                searchCars();
            }
        });
    }
});

// Search cars function
function searchCars() {
    const searchInput = document.getElementById("search-input").value.toLowerCase();

    // Get all car cards
    const carCards = document.querySelectorAll(".car-card");

    // Hide/show cards based on search term
    carCards.forEach(card => {
        const carName = card.querySelector('p').textContent.toLowerCase();
        if (carName.includes(searchInput)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Toggle sub-filter buttons
function toggleSubFilter(btn, category, value) {
    // Remove active class from all buttons in the same category
    document.querySelectorAll(`.sub-filter-btn[data-category='${category}']`).forEach(
        button => button.classList.remove("active")
    );

    // Toggle active class on clicked button
    btn.classList.toggle("active");
    btn.setAttribute("data-category", category);
    btn.setAttribute("data-value", value);

    // Apply filters
    filterCars();
}

// Apply filters to car cards
function filterCars() {
    // Get all active filters
    const activeBodyTypes = Array.from(document.querySelectorAll(".sub-filter-btn.active[data-category='bodyType']"))
        .map(el => el.getAttribute("data-value"));

    const activePrices = Array.from(document.querySelectorAll(".sub-filter-btn.active[data-category='price']"))
        .map(el => el.getAttribute("data-value"));

    const activeTransmissions = Array.from(document.querySelectorAll(".sub-filter-btn.active[data-category='transmission']"))
        .map(el => el.getAttribute("data-value"));

    // Get all car cards
    const carCards = document.querySelectorAll(".car-card");

    // Filter cards based on selected criteria
    carCards.forEach(card => {
        let shouldShow = true;

        // Body type filtering
        if (activeBodyTypes.length > 0) {
            const bodyType = card.getAttribute("data-body-type");
            if (!activeBodyTypes.includes(bodyType)) {
                shouldShow = false;
            }
        }

        // Price filtering
        if (shouldShow && activePrices.length > 0) {
            const price = parseInt(card.getAttribute("data-price"));
            let priceMatch = false;

            for (const priceValue of activePrices) {
                if (priceValue === "500000" && price < 500000) {
                    priceMatch = true;
                } else if (priceValue === "1000000" && price >= 500000 && price < 1000000) {
                    priceMatch = true;
                } else if (priceValue === "1500000" && price >= 1000000 && price < 1500000) {
                    priceMatch = true;
                } else if (priceValue === "2000000" && price >= 1500000 && price < 2000000) {
                    priceMatch = true;
                } else if (priceValue === "3000000" && price > 2000000) {
                    priceMatch = true;
                }
            }

            if (!priceMatch) {
                shouldShow = false;
            }
        }

        // Transmission filtering
        if (shouldShow && activeTransmissions.length > 0) {
            const transmission = card.getAttribute("data-transmission");
            if (!activeTransmissions.includes(transmission)) {
                shouldShow = false;
            }
        }

        // Show/hide car card
        card.style.display = shouldShow ? "block" : "none";
    });
}

// Show all cars
function showAllCars(btn) {
    resetFilterButtons();
    btn.classList.add("active");
    document.querySelectorAll(".sub-filters").forEach(filter => filter.style.display = "none");

    // Show all car cards
    document.querySelectorAll(".car-card").forEach(card => {
        card.style.display = "block";
    });
}

// Show body type filters
function showBodyTypeFilters(btn) {
    resetFilterButtons();
    btn.classList.add("active");
    document.querySelector("#bodyTypeFilters").style.display = "flex";
    document.querySelector("#priceFilters").style.display = "none";
    document.querySelector("#transmissionFilters").style.display = "none";
}

// Show price filters
function showPriceFilters(btn) {
    resetFilterButtons();
    btn.classList.add("active");
    document.querySelector("#priceFilters").style.display = "flex";
    document.querySelector("#bodyTypeFilters").style.display = "none";
    document.querySelector("#transmissionFilters").style.display = "none";
}

// Show transmission filters
function showTransmissionFilters(btn) {
    resetFilterButtons();
    btn.classList.add("active");
    document.querySelector("#transmissionFilters").style.display = "flex";
    document.querySelector("#bodyTypeFilters").style.display = "none";
    document.querySelector("#priceFilters").style.display = "none";
}

// Reset filter buttons
function resetFilterButtons() {
    document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelectorAll(".sub-filter-btn").forEach(btn => btn.classList.remove("active"));
}

// Function to show car variants in modal
function showCarDetails(carId, carModel) {
    const modal = document.getElementById('variantsModal');
    const modalTitle = document.getElementById('modalTitle');
    const variantsContainer = document.getElementById('variantsContainer');

    // Set modal title
    modalTitle.textContent = `${carModel} Variants`;

    // Clear previous variants
    variantsContainer.innerHTML = '<p>Loading variants...</p>';

    // Show modal
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';

    // Here we would fetch car variant data from the server
    // For now, just show a placeholder message
    setTimeout(() => {
        variantsContainer.innerHTML = `
            <p>Variant data for ${carModel} will be loaded from the database.</p>
            <p>Car ID: ${carId}</p>
        `;
    }, 1000);
}

// Function to close modal
function closeModal() {
    const modal = document.getElementById('variantsModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Toggle user menu
function toggleMenu() {
    const menu = document.getElementById("userMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// Close the menu if clicked outside
window.onclick = function (event) {
    const menu = document.getElementById("userMenu");
    const icon = document.querySelector(".profile-icon");
    if (event.target !== icon && !icon.contains(event.target) && menu) {
        menu.style.display = "none";
    }

    // Close modal when clicking outside content
    const modal = document.getElementById('variantsModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    // Add click event to all car cards
    document.querySelectorAll('.car-card').forEach(card => {
        card.addEventListener('click', function () {
            const carId = this.getAttribute('data-car-id');
            const carModel = this.querySelector('p').textContent;
            showCarDetails(carId, carModel);
        });
    });

    // Initialize first filter button as active
    const allButton = document.querySelector('.filter-btn');
    if (allButton) {
        allButton.classList.add('active');
    }
});