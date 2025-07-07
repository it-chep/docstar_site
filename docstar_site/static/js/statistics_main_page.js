



function getStatistics() {
    const loader = $('.statistics_loader')
    $.ajax({
        url: `/api/v1/settings/`,
        method: 'GET',
        success: function (response) {
            const number_of_doctors_container = $('#number_of_doctors')
            const number_of_subs_tg_container = $('#number_of_subs_tg')

            const target = $('.statistics')

            loader.addClass('hidden')
            target.addClass('show')

            const {doctors_count, subscribers_count} = response;
            number_of_doctors_container.text(`${doctors_count}`)
            number_of_subs_tg_container.text(`${subscribers_count}`)
        },
        error: function (xhr, status, error) {
            loader.remove()
            console.error('Ошибка при запросе статистики:', error);
        }
    });
}

$(document).ready(function () {
    getStatistics()
});