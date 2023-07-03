const popup = document.querySelector('.popup');
const closeBtn = popup.querySelector('.close');
const end_popup = document.querySelector('.end_popup');
const closeendbtn = end_popup.querySelector('.end_close');
console.log('1234567890')


document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = document.querySelector('form');
    const formData = new FormData(form);
    const password = formData.get('password');
    const input_div = document.getElementById('email');
    const error = document.getElementById('error-email');
    const currentUrl = window.location.href;
    const email = formData.get('email');


    if (document.getElementById('signup_popup')) {

        fetch(currentUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({password: password, email: email})
        }).then(response => {

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }

        }).then(data => {
            if (data.status === 200) {
                end_popup.style.display = 'block';
                // console.log(data)

            } else if (data.status === 'error') {
                // console.log(input_div);
                if (input_div.classList.contains('input_off')) {
                    input_div.classList.replace('input_off', 'input_on');
                }
                if (error.classList.contains('off')) {
                    error.classList.replace('off', 'on');
                }
            } else if (data.status === 'fatal_error') {
                popup.style.display = 'block';
            }
        }).catch(error => {
            console.error(error);
        });

    } else {
        fetch(currentUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email: email, password: password})
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }

        }).then(data => {
            const signup_btn = document.getElementById('signup_btn');
            const signup_warning = document.getElementById('signup_warning');
            const line = document.getElementById('line');
            if (data.status === 'error') {
                if (input_div.classList.contains('input_off')) {
                    input_div.classList.replace('input_off', 'input_on');
                }
                if (error.classList.contains('off')) {
                    error.classList.replace('off', 'on');
                    signup_btn.classList.replace('off', 'on');
                    signup_warning.classList.replace('off', 'on');
                    line.classList.replace('off', 'on');
                }
            } else if (data.status === 'not_phone') {
                alert('Вы не указали номер телефона!');
            } else if (data.status === 'invalid_data') {
                const pass_div = document.getElementById('password');
                if (pass_div.classList.contains('pass_input_off')) {
                    pass_div.classList.replace('pass_input_off', 'pass_input_on');
                }
                if (error.classList.contains('off')) {
                    const error_password = document.getElementById('error-pass')
                    error_password.classList.replace('off', 'on');
                    signup_btn.classList.replace('off', 'on');
                    signup_warning.classList.replace('off', 'on');
                    line.classList.replace('off', 'on');
                }
            }
        }).catch(error => {
            console.error(error);
        });
    }
});

function closePopup() {
    popup.style.display = 'none';
}

function closeEndPopup() {
    end_popup.style.display = 'none';
}

// Слушаем событие клика на кнопке закрытия попапа
closeBtn.addEventListener('click', closePopup);
closeendbtn.addEventListener('click', closeEndPopup);
