function renderPagination(currentPage, totalPages) {
    const $paginationContainer = $('.pagination_container');
    $paginationContainer.empty();
    if (currentPage === 0 && totalPages === 0) {
        return
    }

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
            setSelectedPageToUrl(currentPage - 1);
            loadDoctors(currentPage - 1);
        });
    }
    if (totalPages - currentPage < 3 && totalPages > 4) {
        $paginationContainer.append(
            `<span class="pagination_button" data-page="1">
                        1
                    </span>`,
            `<span class="pagination_dots">...</span>`
        );
        let startPage = Math.max(1, totalPages - 3);
        for (let i = startPage; i <= totalPages; i++) {
            const pageButton = `
                <span class="pagination_button ${i === currentPage ? 'active' : ''}" data-page="${i}">
                    ${i}
                </span>
            `;
            $paginationContainer.append(pageButton);
            pagesCounter++
        }
    } else {
        let startPage = Math.max(1, currentPage - 1);
        for (let i = startPage; i <= totalPages; i++) {
            if (pagesCounter === 0 && currentPage === 3) {
                $paginationContainer.append(
                    `<span class="pagination_button" data-page="1">
                        1
                    </span>`,
                );
                pagesCounter++
            }

            if (pagesCounter === 0 && currentPage !== 2 && currentPage !== 1) {
                $paginationContainer.append(
                    `<span class="pagination_button" data-page="1">
                        1
                    </span>`,
                    `<span class="pagination_dots">...</span>`
                );
                pagesCounter++
            }

            if (pagesCounter === 5) {
                break;
            }

            if (pagesCounter === 4 && i !== totalPages) {
                $paginationContainer.append(
                    `<span class="pagination_dots">...</span>`,
                    `<span class="pagination_button" data-page="${totalPages}">
                        ${totalPages}
                    </span>`
                );
                pagesCounter++
                continue
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
            setSelectedPageToUrl(currentPage + 1);
            loadDoctors(currentPage + 1);
        });
    }
    $('.pagination_button').on('click', function () {
        const page = $(this).data('page');
        setSelectedPageToUrl(page);
        loadDoctors(page);
    });
}

function setSelectedPageToUrl(page) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.history.pushState({}, '', url);
}