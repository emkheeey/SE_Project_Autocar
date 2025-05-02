// Global variables
let activeFieldId = null;

// Handle profile image upload
document.addEventListener('DOMContentLoaded', function () {
    const profileUpload = document.getElementById('profileUpload');

    if (profileUpload) {
        profileUpload.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    document.getElementById('profileImage').src = e.target.result;

                    // In a real application, you would upload the file to your server here
                    // For now, we'll just simulate a successful upload
                    console.log("Image would be uploaded to server");
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// Edit field function
function editField(fieldId) {
    const modal = document.getElementById('editModal');
    const input = document.getElementById('editInput');
    const fieldTitle = document.getElementById('editFieldTitle');
    const currentValue = document.getElementById(fieldId).textContent;

    // Set active field
    activeFieldId = fieldId;

    // Set up modal
    if (fieldId === 'userName') {
        fieldTitle.textContent = 'Edit Name';
        input.type = 'text';
        input.value = currentValue;
    } else if (fieldId === 'userPassword') {
        fieldTitle.textContent = 'Change Password';
        input.type = 'password';
        input.value = '';
        input.placeholder = 'Enter new password';
    }

    // Show modal
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Handle form submission
document.addEventListener('DOMContentLoaded', function () {
    const editForm = document.getElementById('editForm');

    if (editForm) {
        editForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const input = document.getElementById('editInput');

            // Update the field
            if (activeFieldId === 'userName') {
                document.getElementById('userName').textContent = input.value;
                // In a real app, you would send this to your server
                console.log("Name update would be sent to server:", input.value);
            } else if (activeFieldId === 'userPassword') {
                document.getElementById('userPassword').textContent = '••••••••';
                // In a real app, you would send this to your server
                console.log("Password update would be sent to server");
            }

            // Close modal
            closeModal();
        });
    }
});

// Close modal when clicking outside
window.addEventListener('click', function (event) {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});