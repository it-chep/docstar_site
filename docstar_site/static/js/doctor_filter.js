function toggleFilter(filterId) {
    let content = document.getElementById(filterId);
    content.classList.toggle('show');
}

function showAll(listId) {
    let list = document.getElementById(listId);
    let items = list.getElementsByTagName('li');
    for (let i = 0; i < items.length; i++) {
        items[i].style.display = 'block';
    }
}

function disableTextSelection(targets){
    targets.forEach(target => {
        target.addEventListener('mousedown', (e) => {
            e.preventDefault()
        })
    })
}

// initializeFilterClickAction инициализация тоглов открывания фильтров "Города", "Специальности"
function initializeFilterClickAction() {
    const cityFilterHeader = document.getElementById('city-filter-header')
    const specialityFilterHeader = document.getElementById('speciality-filter-header')
    const subscribersFilterHeader = document.getElementById('subscribers-filter-header')

    disableTextSelection([cityFilterHeader, specialityFilterHeader, subscribersFilterHeader, ...document.querySelectorAll('.checkbox-label')])

    cityFilterHeader.addEventListener('click', function (e) {
        e.preventDefault()
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('city-filter', this);
    });

    specialityFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('speciality-filter', this);
    });

    subscribersFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('subscribers-filter', this);
    });
}

function showFiltersBySearchText(object, searchText) {
    const labelText = object.find('.checkbox-text').text().toLowerCase();

    if (labelText.includes(searchText)) {
        object.show();
    } else {
        object.hide();
    }
}

// initializeSearchFiltersInput инициализация поиска фильтров "Города", "Специальности"
function initializeSearchFiltersInput() {
    const citySearchInput = $('#citySearchInput')
    const cityList = $('#city-list .checkbox-label')

    const specialitySearchInput = $('#specialitySearchInput')
    const specialityList = $('#speciality-list .checkbox-label');

    citySearchInput.on('input', function (event) {
        const searchText = $(this).val().toLowerCase();
        cityList.each(function () {
            showFiltersBySearchText($(this), searchText)
        });

    })

    specialitySearchInput.on('input', function () {
        const searchText = $(this).val().toLowerCase();

        specialityList.each(function () {
            showFiltersBySearchText($(this), searchText)
        });
    });
}

// closeMobileFilterSidebar убирает на мобилке шторку фильтров
function closeMobileFilterSidebar() {

    const windowWidth = $(window).width();
    if (windowWidth < 450) {
        $('.filters_wrapper').fadeOut(300);
    }
}

// resetSubscribersFilter очистка фильтра подписчиков
function resetSubscribersFilter() {
    const $rangeInput = $(".range-input input");
    const $subscribersInput = $(".subscribers-input input");
    const $range = $(".slider .progress");
    const maxAllowed = parseInt($rangeInput.eq(1).attr('max')) || 10000;

    // Очищаем поля ввода
    $subscribersInput.val('');

    // Сбрасываем слайдер к начальным значениям
    const initialMin = 0;
    const initialMax = maxAllowed;

    $rangeInput.eq(0).val(initialMin);
    $rangeInput.eq(1).val(initialMax);

    // Сбрасываем прогресс-бар
    $range.css({
        'left': '0%',
        'right': '0%'
    });
}


// initializeCleanFilterBtn инициализация кнопки "Очистить" фильтры
function initializeCleanFilterBtn() {
    const clearBtn = $('.clear_button');

    clearBtn.on('click', function (event) {

        closeFilter()

        // очищаем фильтры над списком врачей
        $('.active_filters_wrapper').empty();
        // убираем чек у всех фильтров
        $(`.checkbox-label`).each(function () {
            $(this).find('input[type="checkbox"]').prop('checked', false);
        });
        // очищаем фильтр подписчиков
        resetSubscribersFilter();
        // убираем фильтры из URL
        clearAllFilters();
        // убираем на мобилке шторку
        closeMobileFilterSidebar();
        // грузим 1 страницу
        filterDoctors(getFilterQueryParams(), 1);
    })
}

// clearAllFilters - полностью очищает фильтры города и специальности из URL
function clearAllFilters() {
    const urlParams = new URLSearchParams(window.location.search);

    urlParams.delete('city');
    urlParams.delete('speciality');
    urlParams.delete('max_subscribers');
    urlParams.delete('min_subscribers');

    const newUrl = urlParams.toString() ? `${window.location.pathname}?${urlParams}` : window.location.pathname;

    history.pushState(null, null, newUrl);
}

function pushQueryParamsToURL() {
    const selectedCities = [];
    const selectedSpecialities = [];

    // Получаем значения подписчиков
    const minSubscribers = $('#min_subscribers').val();
    const maxSubscribers = $('#max_subscribers').val();

    // Собираем ID выбранных городов
    $('.checkbox-label.city input[type="checkbox"]:checked').each(function () {
        selectedCities.push($(this).data('id'));
    });

    // Собираем ID выбранных специальностей
    $('.checkbox-label.speciality input[type="checkbox"]:checked').each(function () {
        selectedSpecialities.push($(this).data('id'));
    });

    // Формируем URL-параметры
    const params = new URLSearchParams();

    if (selectedCities.length > 0) {

        params.append('city', selectedCities.join(','));
    }

    if (selectedSpecialities.length > 0) {
        params.append('speciality', selectedSpecialities.join(','));
    }

    // Добавляем параметры подписчиков, если они указаны
    if (minSubscribers && minSubscribers.trim() !== '') {
        params.append('min_subscribers', minSubscribers);
    }

    if (maxSubscribers && maxSubscribers.trim() !== '') {
        params.append('max_subscribers', maxSubscribers);
    }

    const newUrl = `${window.location.pathname}?${params.toString()}`;

    // Меняем URL в адресной строке (без перезагрузки)
    history.pushState(null, null, newUrl);
}

function closeFilter(){
    filter_wrapper_mobile_open=false
    removeCheckDisplay()
    const body = document.querySelector('body')
    body.style.overflow=''
}

function setFiltersInlineWrapper(){
    const urlParams = new URLSearchParams(window.location.search);

    const cities = urlParams.get('city')?.split(',')
    cities?.forEach(paramCity => {
        $(`#city-${paramCity}`).prop('checked', true)
    })
    const specialities = urlParams.get('speciality')?.split(',')
    specialities?.forEach(paramSpeciality => {
        $(`#speciality-${paramSpeciality}`).prop('checked', true)
    })
    const page = urlParams.get('page') || 1
    setActiveFilters()
    filterDoctors(getFilterQueryParams(), page);
}


function setActiveFilters(){
    $('.filters-inline-wrapper input[type="checkbox"]:checked').each(function () {
        const checkbox = $(this);
        const labelText = checkbox.closest('.checkbox-label').find('.checkbox-text').text();
        const className = checkbox.closest('.checkbox-label').hasClass('speciality') ? 'speciality' : 'city';
        const ID = checkbox.closest('.checkbox-label').find('input').data('id')

        // Добавляем фильтр в active_filters_wrapper
        $('.active_filters_wrapper').append(`
            <div class="active_filter" data-${className}="${ID}">
                <p class="active_filter_text" >${labelText}</p>
                <div class="active_filter_delete_btn">
                    <span class="material-icons cancel">cancel</span>
                </div>
            </div>
        `);
    });
}


// initializeSubmitFilterBtn инициализация кнопки "Применить" фильтры
function initializeSubmitFilterBtn() {
    const submitButton = $('.submit_button');

    submitButton.on('click', function (event) {
        event.preventDefault();

        closeFilter()

        // Очищаем текущие активные фильтры
        $('.active_filters_wrapper').empty();

        // Собираем все выбранные чекбоксы из filters-inline-wrapper
        setActiveFilters()

        // пушим параметры в URL пользователя
        pushQueryParamsToURL()

        // Применяем фильтры

        filterDoctors(getFilterQueryParams(), 1);

        // убираем на мобилке шторку
        closeMobileFilterSidebar();
    })
}

// cleanFilterQueryParam получает объект чекбокса специальности или города
function cleanFilterQueryParam(checkbox) {
    const $checkbox = $(checkbox);

    // "city-1" или "speciality-3"
    const id = $checkbox.attr('id');
    const [type, value] = id.split('-');

    // получаем параметр
    const urlParams = new URLSearchParams(window.location.search);
    const currentValues = urlParams.get(type)?.split(',') || [];

    const updatedValues = currentValues.filter(v => v !== value);

    // чистим параметры
    if (updatedValues.length > 0) {
        urlParams.set(type, updatedValues.join(','));
    } else {
        urlParams.delete(type);
    }

    // удаляем из урла
    const newUrl = urlParams.toString() ? `${window.location.pathname}?${urlParams.toString()}` : window.location.pathname;
    history.pushState(null, null, newUrl);
}

$(document).ready(function () {
    setFiltersInlineWrapper()
    // инициализация тоглов открывания фильтров "Города", "Специальности"
    initializeFilterClickAction();
    // инициализация поиска фильтров "Города", "Специальности"
    initializeSearchFiltersInput();
    // инициализация кнопки "Очистить" фильтры
    initializeCleanFilterBtn();
    // инициализация кнопки "Применить" фильтры
    initializeSubmitFilterBtn();

    sortList("city-list");
    sortList("speciality-list");

    $(document).on('click', '.active_filter_delete_btn', function (event) {

        const text = $(this).siblings('.active_filter_text').text();
        $(this).parent('.active_filter').remove();
        $(`.checkbox-label`).each(function () {
            if ($(this).find('.checkbox-text').text() === text) {
                let checkbox = $(this).find('input[type="checkbox"]')
                cleanFilterQueryParam(checkbox);
                checkbox.prop('checked', false);
            }
        });

        const className = $(this).hasClass('speciality') ? 'speciality' : 'city';
        handleFilterClick.call(this, event, className);
    });
});

function sortList(listId) {
    let list = document.getElementById(listId);
    let items = list.getElementsByTagName('li');
    let itemsArray = Array.prototype.slice.call(items);
    itemsArray.sort(function (a, b) {
        let textA = a.textContent.trim().toUpperCase();
        let textB = b.textContent.trim().toUpperCase();
        return textA.localeCompare(textB);
    });
    for (let i = 0; i < itemsArray.length; i++) {
        list.appendChild(itemsArray[i]);
    }
}

function getFilterQueryParams() {

    const filters = {};

    $('.active_filters_wrapper .active_filter').each(function () {
        const filterData = $(this).data();

        for (const [key, value] of Object.entries(filterData)) {
            if (!filters[key]) {
                filters[key] = [];
            }
            filters[key].push(value);
        }
    });

    // Добавляем минимальное количество подписчиков
    const minSubscribers = $('#min_subscribers').val();
    if (minSubscribers && minSubscribers.trim() !== '') {
        filters.min_subscribers = [minSubscribers];
    }

    // Добавляем максимальное количество подписчиков
    const maxSubscribers = $('#max_subscribers').val();
    if (maxSubscribers && maxSubscribers.trim() !== '') {
        filters.max_subscribers = [maxSubscribers];
    }

    // Формируем query string
    return Object.entries(filters)
        .map(([key, values]) => {
            // Для числовых параметров подписчиков не кодируем значения
            if (key === 'min_subscribers' || key === 'max_subscribers') {
                return `${key}=${values.join('')}`;
            }
            // Для остальных параметров применяем encodeURIComponent
            return `${key}=${encodeURIComponent(values.join(','))}`;
        })
        .join('&');
}

function handleFilterClick(event, className) {
    event.preventDefault();

    const checkbox = $(this).find('input[type="checkbox"]');
    const labelText = $(this).find('.checkbox-text').text();
    const ID = checkbox.data('id')

    checkbox.prop('checked', !checkbox.prop('checked'));
    if (checkbox.prop('checked')) {
        $('.active_filters_wrapper').append(`
                <div class="active_filter" data-${className}="${ID}">
                    <p class="active_filter_text">${labelText}</p>
                    <div class="active_filter_delete_btn">
                        <span class="material-icons cancel">
                        cancel
                        </span>
                    </div>
                </div>
            `);
    } else {
        $(`.active_filters_wrapper .active_filter[data-${className}="${ID}"]`).remove();
    }

    filterDoctors(getFilterQueryParams(), 1);
}

function pageUp(){
     window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function loaderWrapper(target){
    target.empty();
    const loaderSpinnerWrapper = `<div class="wrapper_loader_spinner">
        <div class="loader_spinner"></div>
    </div>`
    target.append(loaderSpinnerWrapper);
}

function filterDoctors(filters, page = 1) {
    const $doctorListContainer = $('.all_doctors');
    pageUp()
    renderPagination(0, 0);
    loaderWrapper($doctorListContainer)
    $.ajax({
        url: `/api/v1/filter-doctor/?${filters}&page=${page}`, method: 'GET', success: function (response) {
            $doctorListContainer.empty();

            if (response.data && response.data.length > 0) {
                response.data.forEach((doctor, ind) => {
                    const doctorCard = `
                        <div class="user_card_wrapper">
                            <div class="user_card">
                                <div class="user_info_wrap">
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
                                    
                                </div>
                                <div class="buttons_wrapper">
                                    ${doctor.tg_subs_count != 0 ? `<div class="subscribers_link_wrapper miniatures">
                                        <a class="subscribers_link" href="${doctor.tg_channel_url}" target="_blank" rel="noopener noreferrer">
                                            <img class="social_icon" src="/static/img/logos/telegram_logo.png">
                                            <div class="subs_text">
                                                <span class="subs_count">${doctor.tg_subs_count}</span>
                                                <span>${doctor.tg_subs_count_text}</span>
                                            </div>
                                            <div class="subs_ico_link">
                                                <img src="/static/img/icons/doc_detail/subs_link_ico.svg">
                                            </div>
                                        </a>
                                    </div>` : ''}
                                    ${doctor.inst_subs_count != 0 ? `<div class="subscribers_link_wrapper miniatures">
                                        <a class="subscribers_link" href="${doctor.inst_url}" target="_blank" rel="noopener noreferrer">
                                            <img class="social_icon" src="/static/img/logos/Instagram_icon.png">
                                            <div class="subs_text">
                                                <span class="subs_count">${doctor.inst_subs_count}</span>
                                                <span>${doctor.inst_subs_count_text}</span>
                                            </div>
                                            <div class="subs_ico_link">
                                                <img src="/static/img/icons/doc_detail/subs_link_ico.svg">
                                            </div>
                                        </a>
                                    </div>` : ''}
                                    <a class="user_info_btn_container" href="${doctor.doctor_url}">
                                        <div class="user_info_btn">
                                            <div class="user_info_btn_text">Подробнее</div>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    `;
                    $doctorListContainer.append(doctorCard);
                });
                renderPagination(response.page, response.pages);
            } else {
                $doctorListContainer.append('<p class="white_text">Доктора не найдены.</p>');
                renderPagination(0, 0);
            }
        }, error: function (xhr, status, error) {
            console.error('Ошибка при фильтрации врачей:', error);
            $doctorListContainer.empty().append('<p class="white_text">Произошла ошибка при загрузке данных.</p>');
        }
    });
}
