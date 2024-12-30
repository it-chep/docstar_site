// Называется main_main, потому что, когда называешь main, в каком-то месте происходит переопределение, поэтому, не мнеять название а брать за галвный файл

$(document).ready(function () {
    const $searchDoctorContainer = $('.search-doctors-container')
    const $searchDoctorInput = $('.search-doctors-input')
    const $modalContent = $('.modal-content');

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

    $searchDoctorInput.on('input', function () {
        const query = $(this).val().trim();

        if (!query) {
            $modalContent.empty();
            return;
        }

        $.ajax({
            url: '/api/v1/search-doctor/',
            method: 'GET',
            data: {query: query},
            success: function (response) {
                $modalContent.empty();

                if (response.data && response.data.length > 0) {
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
                        $modalContent.append(doctorCard);
                    });
                } else {
                    $modalContent.append('<p>Нет подходящих врачей.</p>');
                }
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при поиске:', error);
                $modalContent.empty().append('<p>Ошибка при загрузке данных.</p>');
            }
        });
    });
})