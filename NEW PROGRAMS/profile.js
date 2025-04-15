// Sample Data (Replace with actual data from backend)
const userData = {
    name: "John Doe",
    email: "johndoe@example.com",
    profilePic: "images/default-profile.png",
    savedFavorites: [
        { id: 1, name: "Toyota Camry SE", image: "images/cars/camry.jpg" },
        { id: 2, name: "Toyota Hillux", image: "images/cars/hillux.jpg" },
        { id: 3, name: "Toyota Fortuner", image: "images/cars/fortuner.jpg" }
    ]
};

// DOM Loaded
document.addEventListener('DOMContentLoaded', function() {
    loadProfile();
    loadFavorites();
});

// Load Profile Data
function loadProfile() {
    document.getElementById('userName').textContent = userData.name;
    document.getElementById('userEmail').textContent = userData.email;
    document.getElementById('profileImage').src = userData.profilePic;
}

// Load Saved Favorites
function loadFavorites() {
    const favoritesGrid = document.getElementById('favoritesGrid');
    favoritesGrid.innerHTML = '';

    if (userData.savedFavorites.length === 0) {
        favoritesGrid.innerHTML = '<p class="no-favorites">No saved favorites yet.</p>';
        return;
    }

    userData.savedFavorites.forEach(car => {
        const card = document.createElement('div');
        card.className = 'favorite-card';
        card.innerHTML = `
            <img src="${car.image}" alt="${car.name}">
            <p>${car.name}</p>
        `;
        card.addEventListener('click', () => viewCarDetails(car.id));
        favoritesGrid.appendChild(card);
    });
}

// Edit Field Function
function editField(fieldId) {
    const field = document.getElementById(fieldId);
    const currentValue = field.textContent;
    
    if (fieldId === 'userPassword') {
        const newPassword = prompt('Enter new password:', '');
        if (newPassword && newPassword.length >= 8) {
            field.textContent = '••••••••';
            // Update password in backend here
            alert('Password updated successfully!');
        } else if (newPassword) {
            alert('Password must be at least 8 characters!');
        }
    } else {
        const newValue = prompt('Edit:', currentValue);
        if (newValue) {
            field.textContent = newValue;
            // Update in backend here
        }
    }
}

// Profile Image Upload
document.getElementById('profileUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('profileImage').src = event.target.result;
            // Upload to backend here
        };
        reader.readAsDataURL(file);
    }
});

// View Car Details
function viewCarDetails(carId) {
    window.location.href = `car-details.html?id=${carId}`;
}

// Logout Function
function logout() {
    if (confirm('Are you sure you want to log out?')) {
        // Clear session/local storage
        localStorage.removeItem('userToken');
        window.location.href = 'login.html';
    }
}