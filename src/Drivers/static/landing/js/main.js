$(document).ready(function() {
    var $data = JSON.parse(localStorage.getItem('plantData'));
    var ctx = document.getElementById("myChart").getContext("2d");
    Chart.defaults.global.legend.display = false;
    //Chart.defaults.global.responsive = false;
    var data = {
        labels: [
            "Озима пшениця",
            "Озимий рапс",
            "Соя",
            "Кукурудза",
            "Соняшник"
        ],
        datasets: [
            {
                data: [27, 23, 26, 8, 16],
                backgroundColor: [
                    "#baa462",
                    "#92d050",
                    "#548235",
                    "#ed7d31",
                    "#ffc000"
                ],
                hoverBackgroundColor: [
                    "#baa462",
                    "#92d050",
                    "#548235",
                    "#ed7d31",
                    "#ffc000"
                ]
            }]
    };
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        height: 200,
        data: data,
        options: {
            animation:{
                animateScale:true,
                responsive:false,
                legend: {
                    fontColor: "#fffff"
                }
            }
        }
    });
});