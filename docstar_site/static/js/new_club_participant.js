$(document).ready(function () {
    $(".submit-button-container").on("click", function () {
        const formData = $("#create-doctor-form").serialize();

        $.ajax({
            url: "/api/v1/create_new_doctor/",
            type: "POST",
            data: formData,
            success: function (response) {
                alert("Анкета успешно отправлена!");
            },
            error: function (response, status, error) {

                const errors = response.responseJSON.errors;
                if (errors) {
                    displayErrors(errors);
                    $('html, body').animate({scrollTop: 0}, 'slow');
                }
                const Alert = response.responseJSON.alert
                if (Alert) {
                    alert(Alert);
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
        placeholder: 'Начните вводить город',
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
        placeholder: 'Начните вводить специальность',
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