var $events = {
    'wheatTillage': 67,
    'wheatSeeding': 75,
    'wheatSpraying': 40,
    'rapeTillage': 65,
    'rapeSeeding': 71,
    'rapeSpraying': 45,
    'soybeanTillage': 85,
    'soybeanSeeding': 41,
    'soybeanSpraying': 52,
    'cornTillage': 92,
    'cornSeeding': 37,
    'cornSpraying': 48,
    'sunflowerTillage': 88,
    'sunflowerSeeding': 33,
    'sunflowerSpraying': 35
}
var $plantData = JSON.parse(localStorage.getItem('obj'));
var $preset = JSON.parse(localStorage.getItem('preset'));

var $eventsArray = Object.entries($events);
$eventsArray.sort(function(a, b) {
    return a[1] - b[1];
});

var $containers = [];

$.each($plantData, function (key, value) {
    if ($preset) {
        if (!$plantData[key] || !$preset[key]) {
            $('*[data-container*="' + key + '"]').detach();
        }
    }
});
$.each($eventsArray, function (i) {
    if ($('*[data-container="' + $eventsArray[i][0] +'"]').length != 0) {
        $containers.splice(i, 0, $eventsArray[i]);
    }
});

function moveEvents(num) {
    $('.b-fake__overlay').css('width', $containers[num][1] + '%');
}
$('.i-container').addClass('js-next');
$.each($containers, function (i) {
    if ($('*[data-container="' + $containers[i][0] +'"]').length == 0) {
        $('*[data-container*="' + $containers[i][0] + '"]').detach();
    }
    $('*[data-point*="' + $containers[i][0] + '"]').css('left', $containers[i][1] + '%');
    $('*[data-point*="' + $containers[i][0] + '"]').css('display', 'block');

})
$('*[data-point*="' + $containers[0][0] + '"]').addClass('js-done');
moveEvents(0);
$('*[data-container="' + $containers[0][0] +'"]').removeClass('js-next').addClass('js-current');

var i = 0;

$('*[data-lang="perform"], *[data-lang="nextAction"]').on('click', function(e) {
    i++;
    if (i +1 <= $containers.length) {
        e.preventDefault();
        $('.i-container').removeClass('js-current').addClass('js-next');
        $('*[data-container*="' + $containers[i][0] + '"]').removeClass('js-next').addClass('js-current');
        moveEvents(i);
        setTimeout(function(){
            $('*[data-point*="' + $containers[i][0] + '"]').addClass('js-done');
        }, 300);
    }
    else {
        console.log('stop');
    }
})

