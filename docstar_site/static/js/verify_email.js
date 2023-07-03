const urlparams = new URLSearchParams(window.location.search);
const email_token = urlparams.get('token')
const mail = urlparams.get('email')

fetch('http://localhost:8000/users/verify_email/get_token', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({email_token: email_token, email: mail})
}).then(response => {

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        return response.json();
    }

})