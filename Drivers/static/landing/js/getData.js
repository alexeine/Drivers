$(document).ready(function () {

    //request to user data
    $.ajax({
        url: '../../static/landing/js'+'user.json',
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

    //request to plant company's data
    $.ajax({
        url: '../../static/landing/js'+'plantData.json',
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

    //request to plant company's data
    $.ajax({
        url: '../../static/landing/js'+'newPlantData.json',
        type: 'get',
        dataType: 'json',
        error: function(data){
        },
        success: function(data){
            var $toSet = data;
            localStorage.setItem('obj', JSON.stringify($toSet));
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

    };

    // takes plant data and sets in to content
    function handlePlantArea(data) {
        var $area = JSON.parse(localStorage.getItem('area'));
        var $plantArea = JSON.parse(localStorage.getItem('plantData'));
        var $newArea = parseFloat($area);
        var $arr = [];

        $.each($plantArea, function(i) {
            var $item = $plantArea[i];
            var $number = Math.floor($newArea / 100 * $item);
            $arr.splice(i, 0, $number);
            $('*[data-target="plantValue"]').eq(i).text($number + ' з ' + $number + ' га'  + ' (100%)');
            $('*[data-target="plantArea"]').eq(i).text($number + ' га');
            $('*[data-target="plantPercent"]').eq(i).text($item + '% площ АПЗ');
        });

        localStorage.setItem('arr', JSON.stringify($arr));
    };

    // initiate preset and setting up starting null values
    var $preset = {};
    $('.preset-input').each(function( i ) {
        $preset[$(this).attr('data-point')] = 100;
    });


    // setting calc data to content and setting up changed nalues
    $('.preset-input').on('input change', function(i) {
        var $oldText = $('*[data-target="plantValue"]').eq($('.preset-input').index( $(this))).html();
        var $newText = $oldText.substr($oldText.indexOf(' ') + 1);
        $newText = $newText.replace(/ *\([^)]*\) */g, "");
        var $thisInputValue = $(this).val();
        var $arr = JSON.parse(localStorage.getItem('arr'));
        var $index = $('.preset-input').index( $(this));
        var $newValue = Math.floor($arr[$index] / 100 * parseInt($thisInputValue)); //maybe Math.round here
        $('*[data-target="plantValue"]').eq($index).text($newValue + ' ' + $newText + ' (' + $thisInputValue + '%)');
        if ($thisInputValue > 0 ) {
            $preset[$(this).attr('data-point')] = $thisInputValue;
        }
        else {
            $preset[$(this).attr('data-point')] = null;
        }
        console.log('!!!!!!', $thisInputValue, $preset);
        localStorage.setItem('preset', JSON.stringify($preset));
    });

    //setting data to content of action
    $('.action-input').on('input change', function() {
        var $thisInputValue = $(this).val();
        var $index = $('.action-input').index( $(this));
        $('*[data-target="paramValue"]').eq($index).text($thisInputValue);
    });



    //small cosmetic change to labels
    $('#switch').on('input change', function () {
        $('.b-settings__info').toggleClass('b-settings__info--current');
    })

})