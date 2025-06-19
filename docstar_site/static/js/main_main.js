// Называется main_main, потому что, когда называешь main, в каком-то месте происходит переопределение, поэтому, не мнеять название а брать за галвный файл

$(document).ready(function () {
    initMobileBurgerAction();
})

function initMobileBurgerAction() {
    const $burgerMenu = $(`
        <div class="mobile_burger">
            <span class="material-icons">
            sort
            </span>
        </div>
    `)

    appendBurgerMenu($burgerMenu);

    $(window).resize(function () {
        $burgerMenu.detach();
        appendBurgerMenu($burgerMenu);
    });

    const $mobileBurger = $('.mobile_burger');
    const $closeMobileBurgerButton = $(
        `<div class="close_mobile_burger_btn">
            <span class="material-icons">
            close
            </span>
        </div>`
    )

    const $burgerBody = $(
        `    
        <div class="burger-wrapper">
            <div class="burger-container">
                <div class="mobile_filter_header">
                    <h1 class="mobile_filter_header_title">Меню</h1>
                </div>
                <div class="mobile_burger_body">
                    <a href="https://medblogers.ru/">Что за клуб?</a>
                    <a href="https://t.me/readydog">Связаться с техподдержкой</a>
                    <a href="https://t.me/Club_Docstar_bot?start=question">Задать вопрос</a>
                </div>
            </div>
        </div>
        `
    )

    $closeMobileBurgerButton.on('click', function () {
        $burgerBody.fadeOut(300)
    });

    $mobileBurger.on('click', function () {
        let $burgerContainer = $('.burger-container')
        if ($burgerContainer.length > 0) {
            if ($burgerContainer.is(':hidden')) {
                $burgerBody.fadeIn(300);
            }
            return;
        }
        $burgerBody.find('.mobile_filter_header').append($closeMobileBurgerButton)
        $('body').append($burgerBody);
        $burgerBody.fadeIn(300);
    })

    $burgerBody.on('click', function () {
        $burgerBody.fadeOut(300)
    })
}

function appendBurgerMenu($burgerMenu) {
    const windowWidth = $(window).width();
    if (windowWidth <= 420) {
        $('.logo-wrapper').append($burgerMenu);
    } else {
        $('.login-container').append($burgerMenu);
    }
}