$(document).ready(function() {
    // Элементы
    const $minRange = $('.range-min');
    const $maxRange = $('.range-max');
    const $minInput = $('#min_subscribers');
    const $maxInput = $('#max_subscribers');
    const $progress = $('.progress');

    // Параметры
    const absoluteMin = 300;    // Минимально возможное значение
    const absoluteMax = 100000; // Максимально возможное значение
    const subscribersGap = 1000; // Минимальный разрыв между значениями

    // Инициализация значений
    $minRange.attr({'min': absoluteMin, 'max': absoluteMax}).val(absoluteMin);
    $maxRange.attr({'min': absoluteMin, 'max': absoluteMax}).val(absoluteMax);
    $minInput.val(absoluteMin);
    $maxInput.val(absoluteMax);

    // Функция обновления прогресс-бара
    function updateProgress(minVal, maxVal) {
        const range = absoluteMax - absoluteMin;
        const left = ((minVal - absoluteMin) / range) * 100;
        const right = 100 - ((maxVal - absoluteMin) / range) * 100;

        $progress.css({
            'left': left + '%',
            'right': right + '%'
        });
    }

    // Обработчики для range-ползунков
    $minRange.on('input', function() {
        let minVal = parseInt($(this).val());
        let maxVal = parseInt($maxRange.val());

        if (maxVal - minVal < subscribersGap) {
            minVal = maxVal - subscribersGap;
            $(this).val(minVal);
        }

        $minInput.val(minVal);
        updateProgress(minVal, maxVal);
    });

    $maxRange.on('input', function() {
        let minVal = parseInt($minRange.val());
        let maxVal = parseInt($(this).val());

        if (maxVal - minVal < subscribersGap) {
            maxVal = minVal + subscribersGap;
            $(this).val(maxVal);
        }

        $maxInput.val(maxVal);
        updateProgress(minVal, maxVal);
    });

    // Обработчики для текстовых полей
    $minInput.on('input', function() {
        let minVal = parseInt($(this).val()) || absoluteMin;
        let maxVal = parseInt($maxInput.val()) || absoluteMax;

        if (minVal < absoluteMin) minVal = absoluteMin;
        if (maxVal - minVal < subscribersGap) minVal = maxVal - subscribersGap;

        $minRange.val(minVal);
        updateProgress(minVal, maxVal);
    });

    $maxInput.on('input', function() {
        let minVal = parseInt($minInput.val()) || absoluteMin;
        let maxVal = parseInt($(this).val()) || absoluteMax;

        if (maxVal > absoluteMax) maxVal = absoluteMax;
        if (maxVal - minVal < subscribersGap) maxVal = minVal + subscribersGap;

        $maxRange.val(maxVal);
        updateProgress(minVal, maxVal);
    });

    // Инициализация прогресс-бара
    updateProgress(absoluteMin, absoluteMax);
});