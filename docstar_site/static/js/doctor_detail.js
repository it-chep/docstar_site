$(document).ready(function() {
    if ($(window).width() <= 768) {
        var $prodoctorov = $('.prodoc_btn_wrapper');
        var $doctorActions = $('.doctor_actions');

        if ($prodoctorov && $doctorActions.length) {
            $doctorActions.append($prodoctorov);
        }
    }
});