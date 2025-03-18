document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "home.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#recommend']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "find.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#browse']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "browse.html"; // Change to your actual landing page URL
});

/**
 * Toggle the user menu visibility
 */
function toggleMenu() {
    const menu = document.getElementById('userMenu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Function to handle logout
function logout() {
    localStorage.removeItem("currentUser");
    alert("Logging out...");
    window.location.href = "login.html";
}

// Mock data for car comparison (replace with actual data)
const carData = {
    camry: { 
        name: "Camry", 
        price: "₽1,200,000", 
        fuelType: "Gasoline", 
        transmission: "Automatic", 
        seats: 5,
        image: "images/cars/camry.jpg"
    },
    hillux: { 
        name: "Hillux", 
        price: "₽1,500,000", 
        fuelType: "Diesel", 
        transmission: "Manual", 
        seats: 5,
        image: "images/cars/hillux.jpg"
    },
    innova: { 
        name: "Innova", 
        price: "₽1,300,000", 
        fuelType: "Diesel", 
        transmission: "Automatic", 
        seats: 7,
        image: "images/cars/innova.jpg"
    },
    vios: { 
        name: "Vios", 
        price: "₽800,000", 
        fuelType: "Gasoline", 
        transmission: "Automatic", 
        seats: 5,
        image: "images/cars/vios.jpg"
    }
};

/**
 * Update car selection display when a car is selected
 * @param {number} carNum - The car selector number (1, 2, or 3)
 */
function updateCarSelection(carNum) {
    const select = document.getElementById('car' + carNum);
    const carImage = document.getElementById('car' + carNum + '-image');
    const cancelBtn = document.getElementById('cancel' + carNum);
    
    if (select.value) {
        // Try to load car image if available
        const carId = select.value;
        const selectedOption = select.options[select.selectedIndex];
        const carName = selectedOption.text;
        
        // First try with model name from the option text
        const modelName = carName.split(' ').slice(2).join('-').toLowerCase();
        carImage.innerHTML = `<img src="/static/images/cars/${modelName}.jpg" 
                             alt="${carName}" 
                             onerror="this.onerror=null; this.src='/static/images/car-placeholder.png';">`;
        
        cancelBtn.style.display = 'inline-block';
    }
}

/**
 * Cancel a car selection
 * @param {number} carNum - The car selector number (1, 2, or 3)
 */
function cancelSelection(carNum) {
    const select = document.getElementById('car' + carNum);
    const carImage = document.getElementById('car' + carNum + '-image');
    const cancelBtn = document.getElementById('cancel' + carNum);
    
    select.value = '';
    carImage.innerHTML = '';
    cancelBtn.style.display = 'none';
}

/**
 * Compare the selected cars by redirecting to the comparison page
 */
function compareCars() {
    const car1 = document.getElementById('car1').value;
    const car2 = document.getElementById('car2').value;
    const car3 = document.getElementById('car3').value;
    
    if (!car1 || !car2) {
        alert('Please select at least two cars to compare');
        return;
    }
    
    // Build query string with selected car IDs
    let queryString = `?car1=${car1}&car2=${car2}`;
    if (car3) {
        queryString += `&car3=${car3}`;
    }
    
    // Redirect to the comparison page with selected cars
    window.location.href = '/cars/compare/' + queryString;
}

// Hide the user menu when clicking outside
document.addEventListener('click', function(event) {
    const userMenu = document.getElementById('userMenu');
    const profileIcon = document.querySelector('.profile-icon');
    
    if (userMenu && userMenu.style.display === 'block' && 
        !userMenu.contains(event.target) && 
        !profileIcon.contains(event.target)) {
        userMenu.style.display = 'none';
    }
});

// Navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Update navigation links
    const homeLink = document.querySelector("a[href='{% url \"home\" %}']");
    if (homeLink) {
        homeLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.getAttribute('href');
        });
    }
});