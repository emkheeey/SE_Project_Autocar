// Toggle user menu function
function toggleMenu() {
    var menu = document.getElementById("userMenu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

// Logout function using POST request
function logout() {
    // Create a form element
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/accounts/logout/';
    
    // Add CSRF token from cookie
    const csrftoken = getCookie('csrftoken');
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrftoken;
    
    // Append to form and submit
    form.appendChild(csrfInput);
    document.body.appendChild(form);
    form.submit();
}

// Function to get CSRF cookie
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

// Close the menu if user clicks outside of it
window.onclick = function(event) {
    var menu = document.getElementById("userMenu");
    var icon = document.querySelector(".profile-icon");
    if (event.target !== icon && !icon.contains(event.target) && 
        event.target !== menu && !menu.contains(event.target)) {
        menu.style.display = "none";
    }
}