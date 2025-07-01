let isLoading = false;

function toggleFilter(filterId) {
    let content = document.getElementById(filterId);
    content.classList.toggle('show');
}


function initializeFilterClickAction(isCity) {
    if(isCity){
        const cityFilterHeader = document.getElementById('city-filter-header')
        disableTextSelection([cityFilterHeader, ...document.querySelectorAll('.checkbox-label.city')])
        cityFilterHeader.addEventListener('click', function () {
            this.querySelector('.filter_open_close_arrow').classList.toggle('open')
            toggleFilter('filter-section-cities', this);
        });
    }
    else{
        const specialityFilterHeader = document.getElementById('speciality-filter-header')
        disableTextSelection([specialityFilterHeader, ...document.querySelectorAll('.checkbox-label.speciality')])
        specialityFilterHeader.addEventListener('click', function () {
            this.querySelector('.filter_open_close_arrow').classList.toggle('open')
            toggleFilter('filter-section-specialties', this);
        });
    }

}

function showFiltersBySearchText(object, searchText) {
    const labelText = object.find('.checkbox-text').text().toLowerCase();
    if (labelText.includes(searchText)) {
        object.show();
    } else {
        object.hide();
    }
}

function disableTextSelection(targets){
    targets.forEach(target => {
        target.addEventListener('mousedown', (e) => {
            e.preventDefault()
        })
    })
}

function initCheckboxCity(){
    $('.checkbox.city').click(function (e) {
        const value = $(this).attr('data-id');
        const text = $(this).attr('text');
        const selectedCities = $('.selected.cities')

        if($(this).prop('checked')){
            if(selectedCities.children().length === 0){
                $('.selected_city').addClass('show')
            }
            selectedCities.append(`
                <li id="li-city-${value}" value=${value}>${text}</li>
            `)
        }
        else{
            if(selectedCities.children().length === 1){
                $('.selected_city').removeClass('show')
            }
            $(`#li-city-${value}`).remove()
        }

    })
}

function initCheckboxSpeciality(){
    $('.checkbox.speciality').click(function (e) {
        const value = $(this).attr('data-id');
        const text = $(this).attr('text');
        const selectedSpecialities = $('.selected.specialities')
        if($(this).prop('checked')){
            if(selectedSpecialities.children().length === 0){
                $('.selected_speciality').addClass('show')
            }
            selectedSpecialities.append(`
                <li id="li-speciality-${value}" value=${value}>${text}</li>
            `)
        }
        else{
            if(selectedSpecialities.children().length === 1){
                $('.selected_speciality').removeClass('show')
            }
            $(`#li-speciality-${value}`).remove()
        }

    })
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

function setInputBorder($target){
    $target.focus(function (){
        $(this).closest('.search-container').addClass('frame')
    })
    $target.blur(function (){
        $(this).closest('.search-container').removeClass('frame')
    })
}

function initCities(){
     $.ajax({
        url: "/api/v1/cities_list/",
        type: "GET",
        success: function (response) {
            $('#additional_cities').append(`
            <div class="filters-inline-wrapper">
                <div id="filter-section-cities" class="filter-section">
                    <div id="city-filter" class="filter-content">
                        <div class="search-container">
                            <img src="/static/img/lupa.svg">
                            <input type="text" id="citySearchInput" placeholder="Найти свой город..." class="search-input">
                        </div>
                        <div class="filter-list" id="city-list">
                            ${response.cities.map(city => 
                                `<label for="city-${city.city_id}" class="checkbox-label city">
                                    <input type="checkbox" text="${city.city_name}"  id="city-${city.city_id}" data-id="${city.city_id}" class="checkbox city">
                                    <span class="checkbox-view">
                                        <img class="checkbox-icon" src="/static/img/homepage/check_mark.svg">
                                    </span>
                                    <p class="checkbox-text">${city.city_name}</p>
                                </label>`
                            ).join('')}
                        </div>
                    </div>
                 
                </div>
            </div>
            `);
            initializeSearchFiltersInput()
            initializeFilterClickAction(true)
            initCheckboxCity()
            setInputBorder($('#citySearchInput'))
        }
    })
}



function initSpecialities(){
     $.ajax({
        url: "/api/v1/specialities_list/",
        type: "GET",
        success: function (response) {
            $('#additional_specialties').append(`
            <div class="filters-inline-wrapper">
                <div id="filter-section-specialties" class="filter-section">
                    <div id="speciality-filter" class="filter-content">
                        <div class="search-container">
                            <img src="/static/img/lupa.svg">
                            <input type="text" id="specialitySearchInput" placeholder="Найти свою специальность..." class="search-input">
                        </div>
                        
                        <div class="filter-list" id="speciality-list">
                            ${response.specialities.map(speciality => 
                                `<label for="speciality-${speciality.speciality_id}" class="checkbox-label speciality">
                                    <input type="checkbox" text="${speciality.speciality_name}" id="speciality-${speciality.speciality_id}" data-id="${speciality.speciality_id}" class="checkbox speciality">
                                    <span class="checkbox-view">
                                        <img class="checkbox-icon" src="/static/img/homepage/check_mark.svg">
                                    </span>
                                    <p class="checkbox-text">${speciality.speciality_name}</p>
                                </label>`
                            ).join('')}
                        </div>
                    </div>
                 
                </div>
            </div>
            `);
            initializeSearchFiltersInput()
            initializeFilterClickAction(false)
            initCheckboxSpeciality()
            setInputBorder($('#specialitySearchInput'))
        }
    })
}

function getSpecialities(){
    let specialities = []
    $('.selected.specialities').children().each((ind, elem) => {
            specialities.push($(elem).attr('value'))
    })
    return specialities.join(',')
}
function getCities(){
    let cities = []
    $('.selected.cities').children().each((ind, elem) => {
            cities.push($(elem).attr('value'))
    })
    return cities.join(',')
}

$(document).ready(function () {


    initCities()
    initSpecialities()
    disableTextSelection([document.querySelector('.checkbox-text')])

    $(".submit-button-container").on("click", function () {
        if(isLoading){
            return
        }
        isLoading = true;
        let formData = $("#create-doctor-form").serialize();
        formData += '&additional_cities=' + getCities()
        formData += '&additional_specialties=' + getSpecialities()

        $.ajax({
            url: "/api/v1/create_new_doctor/",
            type: "POST",
            data: formData,
            success: function (response) {
                isLoading = false;
                window.location.href = response.redirect_url;
            },
            error: function (response, status, error) {
                isLoading = false;
                const errors = response.responseJSON.errors;
                if (errors) {
                    displayErrors(errors);
                    $('html, body').animate({scrollTop: 0}, 'slow');
                }
                const Alert = response.responseJSON.alert
                if (Alert) {
                    console.log(Alert);
                }

            },
        });
    });

    initSelect2Fields();
});

function displayErrors(errors) {
    $(".error-message").remove();
    $(".input-wrapper.error").removeClass('error');

    for (const [field, messages] of Object.entries(errors)) {
        const errorMessage = messages.join(", ");
        const inputElement = $(`[name=${field}]`);
        const inputWrapper = inputElement.closest('.input-wrapper')
        inputWrapper.addClass('error')
        if (inputElement.length) {
            inputWrapper.after(`<div class="error-message">${errorMessage}</div>`);
        }
    }
}

function initSelect2Fields() {
    $('[name=city]').select2({
        width: '100%',
        theme: 'dark',
        language: 'ru',
        placeholder: 'Нажмите чтобы открыть поиск города',
        ajax: {
            url: '/api/v1/select2/cities/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term || '',
                };
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (city) {
                        return {
                            id: city.id,
                            text: city.name
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1,
    });

    $('[name=speciallity]').select2({
        width: '100%',
        theme: 'dark',
        language: 'ru',
        placeholder: 'Нажмите чтобы открыть поиск специальности',
        ajax: {
            url: '/api/v1/select2/specialities/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term || '',
                };
            },
            processResults: function (data) {
                return {
                    results: data.results.map(function (speciality) {
                        return {
                            id: speciality.id,
                            text: speciality.name
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 1,
    });
    $(document).on('select2:open', function (e) {
        $('.select2-search__field').attr('placeholder', 'Введите текст для поиска...');
        setTimeout(() => {
            const searchField = document.querySelector('.select2-search__field');
            if (searchField) {
                searchField.focus();
            }
        }, 0);
    });
}

function initDatePickerField() {
    $('.datepicker').datepicker({
        format: 'dd.mm.yyyy', // Формат даты
        autoclose: true,      // Закрывать календарь после выбора
        todayHighlight: true, // Подсветка текущей даты
        language: 'ru',       // Локализация на русский
        endDate: '0d'         // Запрет выбора будущих дат
    });
}