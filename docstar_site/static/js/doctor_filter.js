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

function initializeFilterClickAction() {
    const cityFilterHeader = document.getElementById('city-filter-header')
    const specialityFilterHeader = document.getElementById('speciality-filter-header')

    cityFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('city-filter', this);
    });

    specialityFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('speciality-filter', this);
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

$(document).ready(function () {
    initializeFilterClickAction();
    initializeSearchFiltersInput();
    sortList("city-list");
    sortList("speciality-list");

    $('.checkbox-label.speciality, .checkbox-label.city').click(function (event) {
        const className = $(this).hasClass('speciality') ? 'speciality' : 'city';
        handleFilterClick.call(this, event, className);
    });

    $(document).on('click', '.active_filter_delete_btn', function (event) {
        const text = $(this).siblings('.active_filter_text').text();
        $(this).parent('.active_filter').remove();
        $(`.checkbox-label`).each(function () {
            if ($(this).find('.checkbox-text').text() === text) {
                $(this).find('input[type="checkbox"]').prop('checked', false);
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

    return Object.entries(filters)
        .map(([key, values]) => `${key}=${encodeURIComponent(values.join(','))}`)
        .join('&')
}

function handleFilterClick(event, className) {
    event.preventDefault();

    const checkbox = $(this).find('input[type="checkbox"]');
    const labelText = $(this).find('.checkbox-text').text();

    checkbox.prop('checked', !checkbox.prop('checked'));
    if (checkbox.prop('checked')) {
        $('.active_filters_wrapper').append(`
                <div class="active_filter" data-${className}="${labelText}">
                    <p class="active_filter_text">${labelText}</p>
                    <img class="active_filter_delete_btn" src="${window.location.origin}/static/img/homepage/cancel_logo.svg">
                </div>
            `);
    } else {
        $(`.active_filters_wrapper .active_filter[data-${className}="${labelText}"]`).remove();
    }

    filterDoctors(getFilterQueryParams(), 1);
}

function filterDoctors(filters, page = 1) {

    const $doctorListContainer = $('.all_doctors');
    $.ajax({
        url: `/api/v1/filter-doctor/?${filters}&page=${page}`,
        method: 'GET',
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
                                        <p>${doctor.speciality}, г. ${doctor.city}</p>
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
                $doctorListContainer.append('<p>Доктора не найдены.</p>');
            }
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при фильтрации врачей:', error);
            $doctorListContainer.empty().append('<p>Произошла ошибка при загрузке данных.</p>');
        }
    });
}
