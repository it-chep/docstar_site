$(document).ready(function () {
    const $searchDoctorContainer = $('.search-doctors-container')
    $searchDoctorContainer.hover(
        function () {
            $(this).find('input').addClass('placeholder-white');
        },
        function () {
            $(this).find('input').removeClass('placeholder-white');
        }
    );

    $searchDoctorContainer.find('input').on('focus', function () {
        $('.search_doctors_modal').show()
    })

    $searchDoctorContainer.find('input').on('blur', function () {
        if (!event.relatedTarget || !event.relatedTarget.classList.contains('mini_doctor_link')) {
            $('.search_doctors_modal').hide()
        }
    })
    $(document).on('click', 'a.mini_doctor_link', function (event) {
        event.preventDefault();
        const href = $(this).attr('href');
        $('.search_doctors_modal').fadeOut(300, function () {
            window.location.href = href;
        });
    });
});