// Называется main_main, потому что, когда называешь main, в каком-то месте происходит переопределение, поэтому, не мнеять название а брать за галвный файл
let burgerWrapper_open = false

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

    const body = document.querySelector('body')
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
        burgerWrapper_open=false
        body.style.overflow=''
        removeCheckScrollForBurgerWrapper()
    });

    $mobileBurger.on('click', function () {
        let $burgerContainer = $('.burger-container')
        burgerWrapper_open=true;
        checkScrollForBurgerWrapper()
        const windowWidth = $(window).width();
        if (windowWidth <= 480) {
            body.style.overflow='hidden';
        }
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

    $burgerBody.on('click', function (e) {
        if(!e.target.closest('.burger-container')){
            $burgerBody.fadeOut(300)
            burgerWrapper_open=false
            body.style.overflow=''
            removeCheckScrollForBurgerWrapper()
        }
    })
}

function appendBurgerMenu($burgerMenu) {
    const windowWidth = $(window).width();
    if (windowWidth <= 900) {
        $('.logo-wrapper').append($burgerMenu);
    } else {
        $('.login-container').append($burgerMenu);
    }
}

function checkResizeForBurgerWrapper(){
    const body = document.querySelector('body')
    const windowWidth = $(window).width();
    if(windowWidth <= 480 && burgerWrapper_open){
        body.style.overflow = 'hidden'
    }
    else{
        body.style.overflow = ''
    }
}

function checkScrollForBurgerWrapper(){
    window.addEventListener('resize', checkResizeForBurgerWrapper)
}

function removeCheckScrollForBurgerWrapper(){
    window.removeEventListener('resize', checkResizeForBurgerWrapper)
}