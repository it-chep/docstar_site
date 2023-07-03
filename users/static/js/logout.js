
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    const currentUrl = window.location.href;
    fetch(currentUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        }
    ).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    }).catch(error => {
            console.error(error);
        });
})