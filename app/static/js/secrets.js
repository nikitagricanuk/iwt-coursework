function addAlert(type, message) {
    // Locate the existing alert container
    const alertContainer = document.querySelector('.alert-container');

    if (alertContainer) {
        // Clear existing alerts
        alertContainer.innerHTML = '';

        // Create a new alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.setAttribute('role', 'alert');
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Append the alert to the container
        alertContainer.appendChild(alert);
    } else {
        console.error('Alert container not found!');
    }
}

function get_secret(secretId) {
    fetch(`${backend_url}/v1/secrets/${secretId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch secret. Please try again later.');
            }
            return response.json();
        })
        .then(data => {
            // Populate offcanvas fields
            document.getElementById('secretName').innerText = data.canonical || 'Unnamed Secret';
            document.getElementById('secretDescription').innerText = data.description || 'No description provided.';
            document.getElementById('secretData').innerText = JSON.stringify(JSON.parse(data.data), null, 2);
            document.getElementById('secretTags').innerText = data.tags.join(', ') || 'No tags.';
            document.getElementById('secretCreatedBy').innerText = data.created_by || 'Unknown';
            document.getElementById('secretCreatedAt').innerText = new Date(data.created_at_timestamp * 1000).toLocaleString();
            document.getElementById('secretExpiresAt').innerText = data.expires_at_timestamp
                ? new Date(data.expires_at_timestamp * 1000).toLocaleString()
                : 'Never';
            document.getElementById('secretStatus').innerText = data.is_disabled ? 'Disabled' : 'Active';
            document.getElementById('secretHash').innerText = data.sha256;

            // Show offcanvas
            const offcanvas = new bootstrap.Offcanvas(document.getElementById('ViewSecretOffCanvas'));
            offcanvas.show();
        })
        .catch(error => {
            addAlert('danger', 'Something went wrong. Reloading the page may resolve the issue.');
        });
}

function delete_secret(secretId) {
    fetch(`${backend_url}/v1/secrets/${secretId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete secret. Please try again later.');
            }
            return response.json();
        })
        .then(data => {
            // Add success alert
            addAlert('success', 'Secret deleted successfully.');
            setTimeout(() => {
                location.reload(); // Reloads the current page
            }, 1000); // Delay to allow the user to see the success message
        })
        .catch(error => {
            // Add error alert
            addAlert('danger', 'Something went wrong. Reloading the page may resolve the issue.');
        });
}