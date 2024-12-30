$(document).ready(function () {

    loadDoctors();

    $(document).on('click', 'a.mini_doctor_link', function (event) {
        event.preventDefault();
        const href = $(this).attr('href');
        $('.search_doctors_modal').fadeOut(300, function () {
            window.location.href = href;
        });
    });

});

function loadDoctors() {
    const $doctorListContainer = $('.all_doctors');

    $.ajax({
        url: '/api/v1/doctor-list',
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
            } else {
                $doctorListContainer.append('<p>Доктора не найдены.</p>');
            }
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при загрузке списка докторов:', error);
            $doctorListContainer.append('<p>Произошла ошибка при загрузке данных.</p>');
        }
    });
}