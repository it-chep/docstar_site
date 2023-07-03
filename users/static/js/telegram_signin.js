document.querySelector('button').addEventListener('submit', function (event) {
    event.preventDefault();

    const input_div = document.getElementById('phone');
    const url = new URLSearchParams(window.location.search);
    const id = url.get('id');
    const name = url.get('first_name') + url.get('last_name')
    const hash = url.get('hash')
    const user_name = url.get('username')

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: id, name: name, hash: hash, user_name: user_name})
    }).then(response => {

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }

    }).then(data => {
        if (data.status === 'not_phone') {
            alert('Человека с таким id не существует, если вы работник и не понимаете ' +
                'в чем ошибка, напишите @maxim_jordan в ТЕЛЕГРАМ')
        }
    }).catch(error => {
        console.error(error);
    });

});
