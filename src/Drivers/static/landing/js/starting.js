$(document).ready(function(){
    var $tag = $('<script></script>');
    $tag.attr('src', 'https://www.youtube.com/iframe_api');
    var $scriptTag = $('script')[2];
    $tag.insertBefore($scriptTag);


    //validating

    $('#email').validate();
});


function onYouTubePlayerAPIReady() {
    player = new YT.Player('video', {
        events: {
            'onReady': onPlayerReady}
    });
}

// 4. The API will call this function when the video player is ready.

function onPlayerReady(event) {
    event.target.mute();
}