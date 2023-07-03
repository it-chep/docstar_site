document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = document.querySelector('form');
    const formData = new FormData(form);
    const email = formData.get('email')
    const token = new URLSearchParams(window.location.search).get('token');
    const password = formData.get('password');
    const currentUrl = window.location.href;
    const input_div = document.getElementById('email');

    fetch(currentUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({password: password, token: token})
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
});

