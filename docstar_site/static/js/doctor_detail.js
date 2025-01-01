$(document).ready(function() {
    if ($(window).width() <= 768) {
        var $societyBlock = $('.society_block');
        var $doctorInfo = $('.doctor_info');

        if ($societyBlock.length && $doctorInfo.length) {
            $doctorInfo.prepend($societyBlock);
        }
    }
});