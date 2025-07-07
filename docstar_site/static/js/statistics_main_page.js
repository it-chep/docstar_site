



function getStatistics() {

    $.ajax({
        url: `/api/v1/settings/`,
        method: 'GET',
        success: function (response) {

            console.log(response)

        },
        error: function (xhr, status, error) {
            console.error('Ошибка при запросе статистики:', error);
        }
    });
}


$(document).ready(function () {
    getStatistics()
});