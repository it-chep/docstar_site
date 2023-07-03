const popup = document.querySelector('.popup');
const closeBtn = popup.querySelector('.close');

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = document.querySelector('form');
    const formData = new FormData(form);
    const email = formData.get('email')
    const currentUrl = window.location.href;
    const input_div = document.getElementById('email');
    const error = document.getElementById('error-email');
    // popup.style.display = 'block';


    fetch(currentUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email})
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    }).then(data => {
        if (data.status === 200) {
            popup.style.display = 'block';
            // console.log(data)
        } else if (data.status === 'error') {
            // console.log(input_div);
            if (input_div.classList.contains('input_off')) {
                input_div.classList.replace('input_off', 'input_on');
            }
            if (error.classList.contains('off')) {
                error.classList.replace('off', 'on');
            }

        }
    })
});


function closePopup() {
    popup.style.display = 'none';
}

// Слушаем событие клика на кнопке закрытия попапа
closeBtn.addEventListener('click', closePopup);
