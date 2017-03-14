$(document).ready(function() {
    $.ajax({
        url: 'js/user.json',
        type: 'get',
        dataType: 'json',
        error: function(data){
        },
        success: function(data){
            handleData(data);
        }
    });
    function handleData(data) {
        console.log('sddsds', data);
        $('#username').text(data.user.name);
        var $allItems = $('[id]');
        $.each( data.user, function( key, value ) {
            console.log( key + ": " + value );
            $('.' + key).text(value);
        });
    }
});