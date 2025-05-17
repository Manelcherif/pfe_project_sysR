document.getElementById('createProfileForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);

    const response = await fetch('/api/candidats/create/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')  // Important !
        }
    });

    const result = await response.json();
    const messageBox = document.getElementById('formMessage');

    if (response.ok) {
        messageBox.innerText = result.message;
        messageBox.style.color = 'green';
        form.reset();
    } else {
        messageBox.innerText = JSON.stringify(result);
        messageBox.style.color = 'red';
    }
});

// Fonction utilitaire pour le CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Cookie commence par le nom recherché
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}