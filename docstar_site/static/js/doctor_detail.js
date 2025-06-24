

function checkWidthForProdoctorovWrap(){
    const $doctor_info = $('.doctor_info');
    const $prodoctorov = $('.prodoc_btn_wrapper');
    const $doctorActions = $('.doctor_actions');

    return function(){
        if ($(window).width() <= 980) {
            if ($prodoctorov && $doctorActions.length) {
                $doctorActions.append($prodoctorov);
            }
        }
        else {
            if ($prodoctorov && $doctorActions.length) {
                $doctor_info.append($prodoctorov);
            }
        }
    }

}

$(document).ready(function() {
    const checkWidthForProdoctorov = checkWidthForProdoctorovWrap()
    checkWidthForProdoctorov()
    $(window).resize(checkWidthForProdoctorov)

});