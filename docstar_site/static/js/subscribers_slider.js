$(document).ready(function () {
    const $rangeInput = $(".range-input input"),
        $subscribersInput = $(".subscribers-input input"),
        $range = $(".slider .progress");

    let subscribersGap = 1000;

    // Обработка ввода в полях подписчиков
    $subscribersInput.on('input', function (e) {
        let minSubscribers = parseInt($subscribersInput.eq(0).val()) || 0,
            maxSubscribers = parseInt($subscribersInput.eq(1).val()) || 0,
            maxAllowed = parseInt($rangeInput.eq(1).attr('max')) || 10000;

        if ((maxSubscribers - minSubscribers >= subscribersGap) && maxSubscribers <= maxAllowed) {
            if ($(this).hasClass('input-min')) {
                $rangeInput.eq(0).val(minSubscribers);
                $range.css('left', (minSubscribers / maxAllowed) * 100 + '%');
            } else {
                $rangeInput.eq(1).val(maxSubscribers);
                $range.css('right', 100 - (maxSubscribers / maxAllowed) * 100 + '%');
            }
        }
    });

    // Обработка ввода в range слайдере
    $rangeInput.on('input', function (e) {
        let minVal = parseInt($rangeInput.eq(0).val()) || 0,
            maxVal = parseInt($rangeInput.eq(1).val()) || 0,
            maxAllowed = parseInt($rangeInput.eq(1).attr('max')) || 10000;

        if ((maxVal - minVal) < subscribersGap) {
            if ($(this).hasClass('range-min')) {
                $rangeInput.eq(0).val(maxVal - subscribersGap);
            } else {
                $rangeInput.eq(1).val(minVal + subscribersGap);
            }
        } else {
            $subscribersInput.eq(0).val(minVal);
            $subscribersInput.eq(1).val(maxVal);
            $range.css({
                'left': (minVal / maxAllowed) * 100 + '%',
                'right': 100 - (maxVal / maxAllowed) * 100 + '%'
            });
        }
    });
});