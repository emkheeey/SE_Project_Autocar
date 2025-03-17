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








// Function to toggle the user menu
function toggleMenu() {
    var menu = document.getElementById("userMenu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
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

// Function to update car selection and display image
function updateCarSelection(carNumber) {
    const selectElement = document.getElementById(`car${carNumber}`);
    const carImageElement = document.getElementById(`car${carNumber}-image`);
    const cancelButton = document.getElementById(`cancel${carNumber}`);
    const selectedCar = selectElement.value;

    if (selectedCar && carData[selectedCar]) {
        carImageElement.innerHTML = `<img src="${carData[selectedCar].image}" alt="${carData[selectedCar].name}">`;
        cancelButton.style.display = "block"; // Show cancel button
    } else {
        carImageElement.innerHTML = "";
        cancelButton.style.display = "none"; // Hide cancel button
    }
}

// Function to cancel car selection
function cancelSelection(carNumber) {
    const selectElement = document.getElementById(`car${carNumber}`);
    const carImageElement = document.getElementById(`car${carNumber}-image`);
    const cancelButton = document.getElementById(`cancel${carNumber}`);
    selectElement.value = "";
    carImageElement.innerHTML = "";
    cancelButton.style.display = "none"; // Hide cancel button
}

// Function to compare cars
function compareCars() {
    const car1 = document.getElementById("car1").value;
    const car2 = document.getElementById("car2").value;
    const car3 = document.getElementById("car3").value;

    const selectedCars = [car1, car2, car3].filter(car => car);

    if (selectedCars.length < 2) {
        alert("Please select at least two cars to compare.");
        return;
    }

    const results = `
        <h3>Comparison Results</h3>
        <table>
            <tr>
                <th>Feature</th>
                ${selectedCars.map(car => `<th>${carData[car].name}</th>`).join("")}
            </tr>
            <tr>
                <td>Price</td>
                ${selectedCars.map(car => `<td>${carData[car].price}</td>`).join("")}
            </tr>
            <tr>
                <td>Fuel Type</td>
                ${selectedCars.map(car => `<td>${carData[car].fuelType}</td>`).join("")}
            </tr>
            <tr>
                <td>Transmission</td>
                ${selectedCars.map(car => `<td>${carData[car].transmission}</td>`).join("")}
            </tr>
            <tr>
                <td>Seats</td>
                ${selectedCars.map(car => `<td>${carData[car].seats}</td>`).join("")}
            </tr>
        </table>
    `;

    document.getElementById("comparisonResults").innerHTML = results;
}

// Close the menu if clicked outside
window.onclick = function(event) {
    var menu = document.getElementById("userMenu");
    var icon = document.querySelector(".profile-icon");
    if (event.target !== icon && !icon.contains(event.target) && event.target !== menu && !menu.contains(event.target)) {
        menu.style.display = "none";
    }
}