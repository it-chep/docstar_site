function renderPagination(currentPage, totalPages) {
    const $paginationContainer = $('.pagination_container');
    $paginationContainer.empty();
    let pagesCounter = 0
    if (currentPage !== 1) {
        const navigationPrev = $(`
            <div class="navigation_btn">
                <span class="material-icons prev">
                    navigate_before
                </span>
            </div>
        `);

        $paginationContainer.append(navigationPrev);

        navigationPrev.on('click', function () {
            loadDoctors(currentPage - 1);
        });
    }

    if (totalPages - currentPage < 5) {
        for (let i = Math.max(1, totalPages - 4); i <= totalPages; i++) {
            const pageButton = `
                <span class="pagination_button ${i === currentPage ? 'active' : ''}" data-page="${i}">
                    ${i}
                </span>
            `;
            $paginationContainer.append(pageButton);
        }
    } else {
        for (let i = currentPage; i <= totalPages; i++) {
            if (pagesCounter === 5) {
                break;
            }
            const pageButton = `
                <span class="pagination_button ${i === currentPage ? 'active' : ''}" data-page="${i}">
                    ${i}
                </span>
            `;
            $paginationContainer.append(pageButton);
            pagesCounter++;
        }
    }

    if (currentPage !== totalPages) {
        const navigationNext = $(`
            <div class="navigation_btn">
                <span class="material-icons next">
                    navigate_next
                </span>
            </div>
        `);

        $paginationContainer.append(navigationNext);

        navigationNext.on('click', function () {
            loadDoctors(currentPage + 1);
        });
    }
    $('.pagination_button').on('click', function () {
        const page = $(this).data('page');
        loadDoctors(page);
    });
}