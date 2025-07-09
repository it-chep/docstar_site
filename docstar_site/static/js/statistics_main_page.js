
function setChecked(){
    const urlParams = new URLSearchParams(window.location.search);
    const subs = urlParams.get('social_media')?.split(',')
    subs?.forEach(paramSub => {
        $(`#sub-${paramSub}`).prop('checked', true)
    })
}

function setSubscribers(res){
    const $filterSectionContainer = $('#filter-section-wrapper')

    const {filter_info} = res;

    if(!filter_info || filter_info.length === 0){
        const $dash = $filterSectionContainer.prev()
        $dash.remove()
        $filterSectionContainer.remove()
    }
    else{
        const $filterSectionSubs = $('#filter-section-subs')
        const $target = $('#subscribers-list')



        filter_info.forEach((sub, ind) => {
            $target.append(`
                <label for="sub-${sub.slug}" class="checkbox-label sub">
                    <input type="checkbox" id="sub-${sub.slug}" data-id="${sub.slug}" class="checkbox">
                    <span class="checkbox-view">
                        <img class="checkbox-icon" src="static/img/homepage/check_mark.svg">
                    </span>
                    <p class="checkbox-text">${sub.name}</p>
                </label>
            `)
        })

        $target.children().each(function () {
            $(this).mousedown(e => e.preventDefault())
        })

        setChecked()

        $filterSectionSubs.addClass('show')
    }
}



function setCounts(res){
    const number_of_doctors_container = $('#number_of_doctors')
    const number_of_subs_tg_container = $('#number_of_subs_tg')

    const target = $('.statistics')

    target.addClass('show')

    const {doctors_count, subscribers_count} = res;

    if(!subscribers_count || subscribers_count === 0){
        const target = number_of_subs_tg_container.closest('.statistic_wrap')
        target.remove()
    }
    else{
        number_of_subs_tg_container.text(`${subscribers_count}`)
    }
    number_of_doctors_container.text(`${doctors_count}`)
}

function getStatistics() {
    const loader = $('.statistics_loader')
    $.ajax({
        url: `/api/v1/settings/`,
        method: 'GET',
        success: function (response) {
            loader.addClass('hidden')
            setCounts(response)
            setSubscribers(response)
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