$(document).ready(function () {
    const $searchDoctorContainer = $('.search-doctors-container')
    const $searchDoctorInput = $('.search-doctors-input')
    const $modalContent = $('.modal-content');
    const $searchDoctorsModal = $('.search_doctors_modal');

    $searchDoctorContainer.hover(
        function () {
            $(this).find('input').addClass('placeholder-white');
        },
        function () {
            $(this).find('input').removeClass('placeholder-white');
        }
    );

    $searchDoctorContainer.find('input').on('focus', function (event) {
        $('.search_doctors_modal').show()
        const element = $('.search-doctors-container')[0];
        const rect = element.getBoundingClientRect();
        const modalContent = $('.modal-content')
        modalContent.css({
            'top': event.target.getBoundingClientRect().top,
            'margin': '75px auto 0'
        });
        if (event.target.getBoundingClientRect().top > rect) {
            modalContent.css({
                'top': rect.top,
                'margin': '75px auto 0'
            });
        }
    })

    $(document).on("scroll", function () {
        const element = $('.search-doctors-container')[0];
        const rect = element.getBoundingClientRect();
        $('.modal-content').css({
            'top': rect.top + 10,
            'margin': '75px auto 0'
        });
    })

    $(document).on('click', function (event) {
        if (
            !$searchDoctorContainer.is(event.target) &&
            !$searchDoctorContainer.has(event.target).length &&
            !$searchDoctorsModal.has(event.target).length
        ) {
            $searchDoctorsModal.hide();
        }
    });

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

                        $(document).on('click', '.mini_doctor_link', function (event) {
                            event.preventDefault();
                            const href = $(this).attr('href');
                            $('.search_doctors_modal').fadeOut(300, function () {
                                window.location.href = href;
                            });
                        });

                        $modalContent.append(doctorCard);
                    });
                } else {
                    $modalContent.append('<div class="mini_user_card"><p class="empty-doctors">Нет подходящих врачей.</p></div>');
                }
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при поиске:', error);
                $modalContent.empty().append('<div class="mini_user_card"><p>Ошибка при загрузке данных.</p></div>');
            }
        });
    });
});