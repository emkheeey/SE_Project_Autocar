document.querySelector("a[href='#home']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "home.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#recommend']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "find.html"; // Change to your actual landing page URL
});

document.querySelector("a[href='#compare-cars']").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default anchor behavior
    window.location.href = "compare.html"; // Change to your actual landing page URL
});



// Sample car data
const cars = [
    { name: "Camry", bodyType: "Sedan", price: 1500000, transmission: "Automatic" },
    { name: "Hillux", bodyType: "Truck", price: 1800000, transmission: "Manual" },
    { name: "Innova", bodyType: "MPV", price: 1200000, transmission: "Automatic" },
    { name: "Vios", bodyType: "Sedan", price: 800000, transmission: "Automatic" },
    { name: "Raize", bodyType: "SUV", price: 900000, transmission: "Automatic" },
    { name: "Noah", bodyType: "MPV", price: 1300000, transmission: "Automatic" },
    { name: "Crown", bodyType: "Sedan", price: 2500000, transmission: "Automatic" },
    { name: "Fortuner", bodyType: "SUV", price: 2200000, transmission: "Automatic" },
    { name: "Corolla", bodyType: "Sedan", price: 1100000, transmission: "Automatic" },
    { name: "GR86", bodyType: "Coupe", price: 2000000, transmission: "Manual" },
    { name: "Atlis", bodyType: "Truck", price: 3000000, transmission: "Automatic" },
    { name: "Avalon", bodyType: "Sedan", price: 2400000, transmission: "Automatic" },
    { name: "RAV4", bodyType: "SUV", price: 1700000, transmission: "Automatic" },
    { name: "Rush", bodyType: "SUV", price: 1000000, transmission: "Automatic" },
    { name: "Supra", bodyType: "Coupe", price: 2800000, transmission: "Automatic" },
    { name: "Sequoia", bodyType: "SUV", price: 3500000, transmission: "Automatic" },
    { name: "Tacoma", bodyType: "Truck", price: 1900000, transmission: "Manual" },
    { name: "Yaris", bodyType: "Hatchback", price: 700000, transmission: "Automatic" },
    { name: "Tundra", bodyType: "Truck", price: 3200000, transmission: "Automatic" },
    { name: "Prius", bodyType: "Hatchback", price: 1600000, transmission: "Hybrid" },
    { name: "Highlander", bodyType: "SUV", price: 2600000, transmission: "Automatic" },
    { name: "Century", bodyType: "Sedan", price: 5000000, transmission: "Automatic" },
    { name: "Land Cruiser", bodyType: "SUV", price: 4000000, transmission: "Automatic" },
    { name: "Alphard", bodyType: "MPV", price: 3000000, transmission: "Automatic" },
    { name: "Roomy", bodyType: "MPV", price: 900000, transmission: "Automatic" },
    { name: "Pixis", bodyType: "Hatchback", price: 600000, transmission: "Automatic" },
    { name: "Aqua", bodyType: "Hatchback", price: 800000, transmission: "Hybrid" },
    { name: "Copen GR Sport", bodyType: "Coupe", price: 1500000, transmission: "Manual" },
    { name: "Mirai", bodyType: "Sedan", price: 3000000, transmission: "Electric" },
    { name: "Hiace", bodyType: "Van", price: 1400000, transmission: "Manual" }
];

// Function to render car cards
function renderCars(filteredCars = cars) {
    const carList = document.getElementById("car-list");
    carList.innerHTML = ""; // Clear existing car cards

    filteredCars.forEach(car => {
        const carCard = document.createElement("div");
        carCard.className = "car-card";
        carCard.innerHTML = `
            <img src="images/cars/${car.name.toLowerCase()}.jpg" alt="${car.name}">
            <p>${car.name}</p>
            <button onclick="viewCar('${car.name}')">View</button>
        `;
        carList.appendChild(carCard);
    });
}

// Initial render
renderCars();

// Search cars function
function searchCars() {
    const searchInput = document.getElementById("search-input").value.toLowerCase();
    const filteredCars = cars.filter(car => car.name.toLowerCase().includes(searchInput));
    renderCars(filteredCars);
}

// Filter cars by body type, price, or transmission
function filterCars() {
    const activeBodyType = document.querySelector(".sub-filter-btn.active[data-category='bodyType']");
    const activePrice = document.querySelector(".sub-filter-btn.active[data-category='price']");
    const activeTransmission = document.querySelector(".sub-filter-btn.active[data-category='transmission']");

    let filteredCars = cars;

    if (activeBodyType) {
        const bodyType = activeBodyType.getAttribute("data-value");
        filteredCars = filteredCars.filter(car => car.bodyType === bodyType);
    }

    if (activePrice) {
        const priceRange = activePrice.getAttribute("data-value");
        const [minPrice, maxPrice] = priceRange.split("-").map(Number);
        filteredCars = filteredCars.filter(car => {
            if (maxPrice) {
                return car.price >= minPrice && car.price <= maxPrice;
            } else {
                return car.price >= minPrice;
            }
        });
    }

    if (activeTransmission) {
        const transmission = activeTransmission.getAttribute("data-value");
        filteredCars = filteredCars.filter(car => car.transmission === transmission);
    }

    renderCars(filteredCars);
}

// Toggle sub-filter buttons
function toggleSubFilter(btn, category, value) {
    const activeBtn = document.querySelector(`.sub-filter-btn.active[data-category='${category}']`);
    if (activeBtn) {
        activeBtn.classList.remove("active");
    }
    btn.classList.toggle("active");
    btn.setAttribute("data-category", category);
    btn.setAttribute("data-value", value);
    filterCars();
}

// Show all cars
function showAllCars(btn) {
    resetFilterButtons();
    btn.classList.add("active");
    document.querySelectorAll(".sub-filters").forEach(filter => filter.style.display = "none");
    renderCars();
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

// Function to handle viewing car details
function viewCar(carModel) {
    window.location.href = `car-details.html?car=${carModel}`;
}

// Toggle user menu
function toggleMenu() {
    const menu = document.getElementById("userMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// Logout function
function logout() {
    localStorage.removeItem("currentUser");
    alert("Logging out...");
    window.location.href = "login.html";
}

// Close the menu if clicked outside
window.onclick = function(event) {
    const menu = document.getElementById("userMenu");
    const icon = document.querySelector(".profile-icon");
    if (event.target !== icon && !icon.contains(event.target) && event.target !== menu && !menu.contains(event.target)) {
        menu.style.display = "none";
    }
}