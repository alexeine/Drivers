$(document).ready(function () {

    //request to user data
    $.ajax({
        url: 'user.json',
        type: 'get',
        dataType: 'json',
        error: function(data){
        },
        success: function(data){
            var $areaToSet = data.user.area;
            localStorage.setItem('area', JSON.stringify($areaToSet));
            handleData(data);
        }
    });

    //request to plant data
    $.ajax({
        url: 'plantData.json',
        type: 'get',
        dataType: 'json',
        error: function(data){
        },
        success: function(data){
            var $toSet = data.plantData;
            localStorage.setItem('plantData', JSON.stringify($toSet));
            handlePlantArea(data);
        }
    });

// takes user data from ajax ant sets it to content
    function handleData(data) {
        $('#username').text(data.user.name);
        var $allItems = $('[data-target]');
        $.each( data.user, function( key, value ) {
            if (key == 'area')
                $('*[data-target="' + key +'"]').text(value.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") + ' ' + 'га');
            else if (key == 'total' || key == 'ebitda' || key == 'investment' || key == 'teamInvestment1' || key == 'teamInvestment1' || key == 'teamInvestment2') {
                $('*[data-target="' + key +'"]').text('$ ' + value.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
            }
            else if (key == 'rentability' || key == 'investmentRentability')
                $('*[data-target="' + key +'"]').text(value.replace(/\./g, ',') + '%');
            else {
                $('*[data-target="' + key +'"]').text(value);
            }
        });
        var $forOneHa = Math.round((parseInt(data.user.ebitda)) / parseInt(data.user.area));
        var $profit = Math.round(parseInt(data.user.investment) / 100 * parseFloat(data.user.investmentRentability));
        var $profitBeautified = $profit.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
        $('*[data-target="ebitdaForHa"]').text('$ ' + $forOneHa.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
        $('*[data-target="profit"]').text('$ ' + $profitBeautified);

    }

    function handlePlantArea(data) {
        var $area = JSON.parse(localStorage.getItem('area'));
        var $plantArea = JSON.parse(localStorage.getItem('plantData'));
        var $newArea = parseFloat($area);
        var $arr = [];
        $('*[data-target="plantValue"]').each(function(i) {
            var $item = $plantArea[i];
            var $number = Math.floor($newArea / 100 * $item);
            $arr.splice(i, 0, $number);
            $(this).text(0 + ' з ' + $number + ' га'  + ' (0%)');
        })
        localStorage.setItem('arr', JSON.stringify($arr));
    }
    $('.input').on('input change', function() {
        var $oldText = $('*[data-target="plantValue"]').eq($('input').index( $(this))).html();
        var $newText = $oldText.substr($oldText.indexOf(' ') + 1);
        $newText = $newText.replace(/ *\([^)]*\) */g, "");
        var $thisInputValue = $(this).val();
        var $arr = JSON.parse(localStorage.getItem('arr'));
        var $index = $('input').index( $(this));
        var $newValue = Math.floor($arr[$index] / 100 * parseInt($thisInputValue)); //maybe Math.round here
        console.log($newValue);
        $('*[data-target="plantValue"]').eq($index).text($newValue + ' ' + $newText + ' (' + $thisInputValue + '%)');
        //console.log('this', $('input').index( $(this)));
        //console.log($('*[data-target="plantValue"]').eq($('input').index( $(this))));
        //console.log($('*[data-target="plantValue"]').eq($('input').index( $(this))).html());
        //$('*[data-target="plantValue"]').eq($('input').index( $(this))).replace($oldValue, 'test')
    });
})