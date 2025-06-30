function loaderSearchModal(target){
    target.empty();
    const loader_spinner = `<div class="loader_spinner"></div>`
    target.append(loader_spinner);
}

$(document).ready(function () {
    const $searchDoctorContainer = $('.search-doctors-container')
    const $searchDoctorInput = $('.search-doctors-input')
    const $modalContent = $('.modal-content');
    const $searchDoctorsModal = $('.search_doctors_modal');
    const $darken = $('.dark-substrate')

    $searchDoctorContainer.hover(
        function () {
            $(this).find('input').addClass('placeholder-white');
        },
        function () {
            $(this).find('input').removeClass('placeholder-white');
        }
    );

    $searchDoctorInput.on('focus', function (event) {
        $searchDoctorsModal.show()
        $('.dark-substrate').show();
    })

    $darken.on('click', function (event) {
        $searchDoctorsModal.hide();
        $('.dark-substrate').hide();
    })

    let xhr = null;

    $searchDoctorInput.on('input', function () {
        const query = $(this).val().trim();

        if(xhr){
            xhr.abort()
            xhr = null;
        }else {
            loaderSearchModal($modalContent)
        }

        if (!query) {
            $modalContent.empty();
            return;
        }

        xhr = $.ajax({
            url: '/api/v1/search-doctor/',
            method: 'GET',

            data: {query: query},
            success: async function (response) {
                $modalContent.empty();
                xhr = null;
                let searchHTML;

                if (
                    (response.cities && response.cities.length > 0) ||
                    (response.specialities && response.specialities.length > 0) ||
                    (response.data && response.data.length > 0)
                ) {
                    searchHTML = '<div class="search-city-spec-container">';
                }

                // Добавляем города, если они есть в ответе
                if (response.cities && response.cities.length > 0) {
                    searchHTML = enrichCitySearch(response, searchHTML)
                }

                // Добавляем специальности, если они есть в ответе
                if (response.specialities && response.specialities.length > 0) {
                    searchHTML = enrichSpecialitySearch(response, searchHTML)
                }

                $modalContent.append(searchHTML);

                if (response.data && response.data.length > 0) {
                    $modalContent.append(`<div class="search-title">Доктора</div>`)

                    response.data.forEach(doctor => {
                        const doctorCard = `
                            <a href="${doctor.doctor_url}" class="mini_doctor_link">
                                <div class="mini_user_card">
                                    <div class="mini_user_avatar">
                                        ${doctor.avatar_url ? `<img class="mini_avatar" src="${doctor.avatar_url}" />` : ''}
                                    </div>
                                    <div class="mini_doctor_info">
                                        <div class="mini_doctor_name">
                                            <p>${doctor.name}</p>
                                        </div>
                                        <div class="mini_additional_info">
                                            <p>${doctor.speciality}, г. ${doctor.city}</p>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        `;

                        $(document).on('click', '.mini_doctor_link', function (event) {
                            event.preventDefault();
                            const href = $(this).attr('href');
                            $('.search_doctors_modal').fadeOut(300, function () {
                                window.location.href = href;
                            });
                        });

                        $modalContent.append(doctorCard);
                    });
                }
                if (response.data.length === 0 && response.specialities.length === 0 && response.cities.length === 0) {
                    $modalContent.append('<div class="mini_user_card"><p class="empty-doctors">Нет подходящих врачей.</p></div>');
                    return
                }

                initSpecialitySearch($searchDoctorsModal);
                initCitySearch($searchDoctorsModal);
            },
            error: function (xhr, status, error) {
                if(error === 'abort'){
                    return
                }
                console.error('Ошибка при поиске:', error);
                $modalContent.empty().append('<div class="mini_user_card"><p>Ошибка при загрузке данных.</p></div>');
            }
        });
    });
});

function enrichCitySearch(response, searchHTML) {
    searchHTML += `
        <div class="search-city">
        <div class="search-title">Города</div>
        <div class="search-items cities-container">
            ${response.cities.map(city => `
                <div class="city-block" data-id="${city.id}">
                    <div class="search-ico">
                        <img src="/static/img/icons/search/city.png">
                    </div>
                    <div class="city-info">
                        <div class="city-name">${city.name}</div>
                        <div class="city-doctors-count">Кол-во врачей: ${city.doctors_count}</div>
                    </div>
                </div>
            `).join('')}
        </div>
        </div>
    `;

    return searchHTML
}

function enrichSpecialitySearch(response, searchHTML) {
    searchHTML += `
    <div class="search-speciality">
        <div class="search-title">Специальности</div>
        <div class="search-items specialities-container">
            ${response.specialities.map(spec => `
                <div class="speciality-block" data-id="${spec.id}">
                    <div class="search-ico">
                        <img src="/static/img/icons/search/speciality.png">
                    </div>
                    <div class="speciality-info">
                        <div class="speciality-name">${spec.name}</div>
                        <div class="speciality-doctors-count">Кол-во врачей: ${spec.doctors_count}</div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>
    `;

    return searchHTML
}

function initSpecialitySearch($searchDoctorsModal) {
    $('.speciality-block').on('click', function (event) {
        event.preventDefault();
        const activeFilterWrapper = $('.active_filters_wrapper')
        const specialityID = $(this).data('id');
        const specialityCheckbox = $(`.checkbox-label.speciality input[data-id="${specialityID}"]`);

        if (specialityCheckbox.length) {
            $('.checkbox-label.city input[type="checkbox"]').prop('checked', false);
            $('.checkbox-label.speciality input[type="checkbox"]').prop('checked', false);
            specialityCheckbox.prop('checked', true);

            clearAllFilters();
            activeFilterWrapper.empty();

            const labelText = specialityCheckbox.closest('.checkbox-label').find('.checkbox-text').text() || $(this).text().trim();

            activeFilterWrapper.append(`
                <div class="active_filter" data-speciality="${specialityID}">
                    <p class="active_filter_text">${labelText}</p>
                    <div class="active_filter_delete_btn">
                        <span class="material-icons cancel">cancel</span>
                    </div>
                </div>
            `);

            pushQueryParamsToURL();

            filterDoctors(getFilterQueryParams(), 1);

            $searchDoctorsModal.hide();
            $('.dark-substrate').hide();
        }
    });
}

function initCitySearch($searchDoctorsModal) {
    $('.city-block').on('click', function (event) {
        event.preventDefault();
        const activeFilterWrapper = $('.active_filters_wrapper')
        const cityID = $(this).data('id');
        const cityCheckbox = $(`.checkbox-label.city input[data-id="${cityID}"]`);

        if (cityCheckbox.length) {
            $('.checkbox-label.city input[type="checkbox"]').prop('checked', false);
            $('.checkbox-label.speciality input[type="checkbox"]').prop('checked', false);
            cityCheckbox.prop('checked', true);

            clearAllFilters();
            activeFilterWrapper.empty();

            const labelText = cityCheckbox.closest('.checkbox-label').find('.checkbox-text').text() || $(this).text().trim();

            activeFilterWrapper.append(`
                <div class="active_filter" data-city="${cityID}">
                    <p class="active_filter_text">${labelText}</p>
                    <div class="active_filter_delete_btn">
                        <span class="material-icons cancel">cancel</span>
                    </div>
                </div>
            `);

            pushQueryParamsToURL();

            filterDoctors(getFilterQueryParams(), 1);

            $searchDoctorsModal.hide()
            $('.dark-substrate').hide();
        }
    })
}