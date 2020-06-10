var ctx = document.getElementById('factor-chart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['国内株式', '国内債券', '先進国株式', '先進国債券'],
        datasets: [{
            label: 'バリュー',
            backgroundColor: "red",
            borderColor: "red",
            borderWidth: 1,
            data: [3.0, 0.5, 3.5, 1.0],
        },
        {
            label: 'サイズ',
            backgroundColor: "blue",
            borderColor: "blue",
            borderWidth: 1,
            data: [-1.0, -0.5, -1.0, -0.5],
        },
        {
            label: 'モメンタム',
            backgroundColor: "green",
            borderColor: "green",
            borderWidth: 1,
            data: [0.2, 0.1, 0.4, 0.1],
        },
        {
            label: 'クオリティ',
            backgroundColor: "yellow",
            borderColor: "yellow",
            borderWidth: 1,
            data: [1.0, 0.4, 1.1, 0.5],
        },
        {
            label: 'その他',
            backgroundColor: "gray",
            borderColor: "gray",
            borderWidth: 1,
            data: [0.1, -0.1, 0.1, -0.1],
        }]
    },
    options: {
        title: {
            display: true,
            text: 'ファクター分解', //グラフの見出し
            padding: 3
        },
        scales: {
            xAxes: [{
                stacked: true, //積み上げ棒グラフにする設定
                categoryPercentage: 0.4 //棒グラフの太さ
            }],
            yAxes: [{
                stacked: true //積み上げ棒グラフにする設定
            }]
        },
        legend: {
            labels: {
                boxWidth: 30,
                padding: 20 //凡例の各要素間の距離
            },
            display: true
        },
        tooltips: {
            mode: 'label' //マウスオーバー時に表示されるtooltip
        }
    },
});
