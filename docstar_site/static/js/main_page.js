$(document).ready(function () {
    loadDoctors(getStartPage());
    initMobileFilterAction();
    resizeMainTitle();
});

function resizeMainTitle() {
    const $mainTitle = $('.main-title');
    relocateMainTitle($mainTitle);
    $(window).resize(function () {
        relocateMainTitle($mainTitle);
    });
}

function relocateMainTitle($mainTitle) {
    const windowWidth = $(window).width();
    if (windowWidth <= 420) {
        $mainTitle.detach().insertAfter('.banner_new_doctor_mobile');
    } else {
        $mainTitle.detach().prependTo('.doctors_container');
    }
}

function initMobileFilterAction() {
    const $filterWrapper = $('.filters_wrapper')

    const $closeMobileFilterButton = $(`<div class="close_mobile_filter_btn">
        <span class="material-icons">
        close
        </span>
    </div>`)

    $closeMobileFilterButton.on('click', function () {
        $filterWrapper.fadeOut(300)
    });

    $('.settings_icon_wrapper').on('click', function () {
        $filterWrapper.fadeIn(300);
        if (!$filterWrapper.find('.mobile_filter_header').length) {
            $filterWrapper.prepend(`
                <div class="mobile_filter_header">
                    <h1 class="mobile_filter_header_title">Фильтры</h1>
                </div>
            `);
            $filterWrapper.find('.mobile_filter_header').append($closeMobileFilterButton);

            const cityFilterHeader = document.getElementById('city-filter-header')
            cityFilterHeader.querySelector('.filter_open_close_arrow').classList.toggle('open')
            toggleFilter('city-filter', cityFilterHeader);

            const specialityFilterHeader = document.getElementById('speciality-filter-header')
            specialityFilterHeader.querySelector('.filter_open_close_arrow').classList.toggle('open')
            toggleFilter('speciality-filter', specialityFilterHeader);
        }
    });
}

function loadDoctors(page) {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    const $doctorListContainer = $('.all_doctors');
    const filterParams = getFilterQueryParams()
    if (filterParams.length !== 0) {
        filterDoctors(filterParams, page)
        return
    }

    $.ajax({
        url: '/api/v1/doctor-list/',
        method: 'GET',
        data: {page: page},
        success: function (response) {
            $doctorListContainer.empty();

            if (response.data && response.data.length > 0) {
                response.data.forEach(doctor => {
                    const doctorCard = `
                            <div class="user_card_wrapper">
                                <div class="user_card">
                                    <div class="user_avatar">
                                        ${doctor.avatar_url ? `<img class="avatar" src="${doctor.avatar_url}" />` : ''}
                                    </div>
                                    <div class="doc_info">
                                        <div class="user_name doctor_name">
                                            <p>${doctor.name}</p>
                                        </div>
                                        <div class="user_additional_info">
                                            <p>${doctor.speciality}</p>
                                            <p>📍${doctor.city}</p>
                                        </div>
                                    </div>
                                    <a class="user_info_btn_container" href="${doctor.doctor_url}">
                                        <div class="user_info_btn">
                                            <div class="user_info_btn_text">Подробнее</div>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        `;
                    $doctorListContainer.append(doctorCard);
                });
                renderPagination(response.page, response.pages);
            } else {
                $doctorListContainer.append('<p class="white_text">Доктора не найдены.</p>');
            }
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при загрузке списка докторов:', error);
            $doctorListContainer.append('<p class="white_text">Произошла ошибка при загрузке данных.</p>');
        }
    });
}

function getStartPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    let currentPage = 1;
    if (pageParam) {
        currentPage = parseInt(pageParam, 10);
    }
    return currentPage
}