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

