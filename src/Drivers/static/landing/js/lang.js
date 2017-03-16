var $current = JSON.parse(localStorage.getItem('lang')) || 'en';

function getLang() {
    $.ajax({
        url: $current + '.json',
        type: 'get',
        dataType: 'json',
        error: function(data){
        },
        success: function(data){
            pick(data.langData);
        }
    });
}

function pick(data) {
    $.each( data, function( key, value ) {
        $('*[data-lang="' + key +'"]').text(value);
    });
}
getLang();
$('.b-picker').on('click',function () {
   $(this).addClass('js-active');
});
$('.b-languages__item').on('click', function () {
    $('.b-picker').removeClass('js-active');
    var $lang = $(this).attr("data-value");
    if ($lang != 'current') {
        localStorage.setItem('lang', JSON.stringify($lang));
        $current = JSON.parse(localStorage.getItem('lang'))
        getLang();
    }
})