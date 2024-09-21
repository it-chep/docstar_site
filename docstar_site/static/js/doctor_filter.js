function toggleFilter(filterId) {
    let content = document.getElementById(filterId);
    content.classList.toggle('show');
}

function showAll(listId) {
    let list = document.getElementById(listId);
    let items = list.getElementsByTagName('li');
    for (let i = 0; i < items.length; i++) {
        items[i].style.display = 'block';
    }
}

function initializeFilterClickAction() {
    const cityFilterHeader = document.getElementById('city-filter-header')
    const specialityFilterHeader = document.getElementById('speciality-filter-header')

    cityFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('city-filter', this);
    });

    specialityFilterHeader.addEventListener('click', function () {
        this.querySelector('.filter_open_close_arrow').classList.toggle('open')
        toggleFilter('speciality-filter', this);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initializeFilterClickAction();
    sortList("city-list");
    sortList("speciality-list");

    $('.checkbox-label.speciality, .checkbox-label.city').click(function (event) {
        const className = $(this).hasClass('speciality') ? 'speciality' : 'city';
        handleFilterClick.call(this, event, className);
    });

    $(document).on('click', '.active_filter_delete_btn', function () {
        const text = $(this).siblings('.active_filter_text').text();
        $(this).parent('.active_filter').remove();
        $(`.checkbox-label`).each(function () {
            if ($(this).find('.checkbox-text').text() === text) {
                $(this).find('input[type="checkbox"]').prop('checked', false);
            }
        });
    });
});

function sortList(listId) {
    let list = document.getElementById(listId);
    let items = list.getElementsByTagName('li');
    let itemsArray = Array.prototype.slice.call(items);
    itemsArray.sort(function (a, b) {
        let textA = a.textContent.trim().toUpperCase();
        let textB = b.textContent.trim().toUpperCase();
        return textA.localeCompare(textB);
    });
    for (let i = 0; i < itemsArray.length; i++) {
        list.appendChild(itemsArray[i]);
    }
}

function handleFilterClick(event, className) {
    event.preventDefault();

    const checkbox = $(this).find('input[type="checkbox"]');
    const labelText = $(this).find('.checkbox-text').text();

    checkbox.prop('checked', !checkbox.prop('checked'));

    if (checkbox.prop('checked')) {
        $('.active_filters_wrapper').append(`
                <div class="active_filter" data-${className}="${labelText}">
                    <p class="active_filter_text">${labelText}</p>
                    <img class="active_filter_delete_btn" src="${window.location.origin}/static/img/homepage/cancel_logo.svg">
                </div>
            `);
    } else {
        $(`.active_filters_wrapper .active_filter[data-${className}="${labelText}"]`).remove();
    }
}
