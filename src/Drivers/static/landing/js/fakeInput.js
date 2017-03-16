console.log('!!!!!', JSON.parse(localStorage.getItem('obj')));

var $obj = JSON.parse(localStorage.getItem('obj'));
var $preset = JSON.parse(localStorage.getItem('preset'));
var $plantData = JSON.parse(localStorage.getItem('plantData'));
var $events = {
    'wheat': {
        'seeding': 67.1
    },
    'rape': {
        'seeding': 81.5
    },
    'soybean': {
        'seeding': 36.1
    },
    'corn': {
        'seeding': 27.4
    },
    'sunflower': {
        'seeding': 30.1
    }
}
var $newArr = [];
$.each( $events, function( key, value ) {
    $.each(value, function (key, value) {
        $newArr.splice(-1, 0, value);
    })
});
$newArr.sort(function(a, b) {
    return a - b;
});
var $now = $newArr[0];
var  $newIndex = 1;

var $sorted = Object.keys($events).sort(function(a,b){return $events[a].seeding-$events[b].seeding});
var $finalData = Object.entries($obj);
$.each($finalData, function (i) {
    $finalData[i][0] = Object.keys($events)[i];
    if ($preset[i]) {
        $finalData[i][1] = $preset[i];
    }
    else {
       $finalData[i][1] = 0;
    }
})
$('.b-fake--overlay').css('width', $now + '%');
$.each(Object.values($obj), function (i) {
    if (Object.values($obj)[i] > 0) {
        $now = $newArr[i];
        if ($preset[i] && $preset[i] > 0) {
            console.log($newArr);
            $('*[data-point="' + Object.keys($events)[i] +'"]').css('display', 'block');
            $('*[data-point="' + Object.keys($events)[i] +'"]').css('left', $now + '%');
            var $width = $('.b-fake--overlay').css('width');
            //$('*[data-container="' + $sorted[0] +'"]').removeClass('js-next').addClass('js-current');
        }
    }
})
var getIndex = 0;
/*$('*[data-lang="perform"]').on('click', function () {
    getIndex++;
    var test = $('*[data-container="' + $sorted[0] +'"]').attr('data-container');
    var newTest = $('.i-container.js-current').attr('data-container');
    function checkItem(item) {
        return item >= newTest;
    }
    console.log($finalData);
    //getIndex = $sorted.findIndex(checkItem);
    //console.log('get index', getIndex);

    if (getIndex < $finalData.length) {
        if ($('*[data-container="' + $sorted[getIndex] +'"]').hasClass('js-hidden')) {
            $('.i-container').removeClass('js-current').addClass('js-next');
            $('*[data-container="' + $sorted[getIndex + 1] +'"]').removeClass('js-next').addClass('js-current');
        }
        else {
            $('.i-container').removeClass('js-current').addClass('js-next');
            $('*[data-container="' + $sorted[getIndex] +'"]').removeClass('js-next').addClass('js-current');
        }
    }
})*/
