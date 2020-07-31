// color params
const colorList = [
    'tomato',
    'cornflowerblue',
    'lightgreen',
    'khaki',
    'darkorange',
    'hotpink',
    'darkgoldenrod',
    'darkred',
    'slategray',
];

// extract colnames from python row colname
function extractColName(colName) {
    colName = colName.split('\'');
    let id = [];
    for (let i = 0; i < colName.length; i++) {
        if (colName[i].length > 2) {
            id.push(colName[i]);
        }
    }
    console.log(id);
    // delete "Date"
    if (colName[0] == 'Date') {
        id = id.slice(1);
    }
    return id;
}

// extract data from python pandas dataframe
function extractData(indexData, sliceNum) {
    let graphLabel = [];
    indexData = indexData.slice(sliceNum);
    for (let i = 0; i < indexData.length; i++) {
        graphLabel.push(indexData[i].split(' ')[0]);
        let id = [];
        let r = indexData[i].split(' ');
        for (let j = 0; j < r.length; j++) {
            if (r[j] !== '') {
                id.push(Number(r[j]));
            }
        }
        indexData[i] = id.slice(1);
    }
    let transpose = a => a[0].map((_, c) => a.map(r => r[c]));
    indexData = transpose(indexData);
    console.log(indexData);
    return [indexData, graphLabel];
}

function makeLineGraph(colId, indexId, graphId, graphTitle, sliceNum) {
    // prepare row data
    let colName = document.getElementById(colId).value;
    let indexData = document.getElementById(indexId).value.split('\n');

    // extract data from row python data
    colName = extractColName(colName);
    const [indexData_, graphLabel_] = extractData(indexData, sliceNum);

    // set graph data
    const allData = [];
    for (let i = 0; i < indexData_.length; i++) {
        allData.push({
            // data
            label: colName[i],
            data: indexData_[i],

            // optional settings
            borderColor: colorList[i],
            backgroundColor: colorList[i],
            borderWidth: 2,
            lineTension: 0,
            pointRadius: 0.5,
            fill: false,
        });
    }
    console.log(indexData_);
    console.log(indexData_.length);

    // main
    const ctx = document.getElementById(graphId).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: graphLabel_,
            datasets: allData,
        },
        options: {
            title: {
                display: true,
                text: graphTitle,
                padding: 5,
            },
            legend: {
                labels: {
                    boxWidth: 30,
                    padding: 20,
                },
                display: true,
            },
            tooltips: {
                mode: 'label',
            },
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 12,
                    }
                }]
            },
        },
    });
    return chart;
}

function makeBarGraph(colId, indexId, graphId, graphTitle, sliceNum) {
    // prepare row data
    let colName = document.getElementById(colId).value;
    let indexData = document.getElementById(indexId).value.split('\n');

    // extract data from row python data
    colName = extractColName(colName);
    const [indexData_, graphLabel_] = extractData(indexData, sliceNum);

    // set graph data
    const allData = [];
    for (let i = 0; i < indexData_.length; i++) {
        allData.push({
            // data
            label: colName[i],
            data: indexData_[i],

            // optional settings
            borderColor: colorList[i],
            backgroundColor: colorList[i],
            borderWidth: 2,
        });
    }
    console.log(indexData_);
    console.log(indexData_.length);

    // main
    const ctx = document.getElementById(graphId).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: graphLabel_,
            datasets: allData,
        },
        options: {
            title: {
                display: true,
                text: graphTitle,
                padding: 5,
            },
            legend: {
                labels: {
                    boxWidth: 30,
                    padding: 20,
                },
                display: true,
            },
            tooltips: {
                mode: 'label',
            },
            scales: {
                xAxes: [{
                    stacked: true, //積み上げ棒グラフにする設定
                    categoryPercentage: 0.4, //棒グラフの太さ
                }],
                yAxes: [{
                    stacked: true, //積み上げ棒グラフにする設定
                    scaleLabel: {                       // 軸ラベル
                        display: true,                  // 表示設定
                        labelString: "寄与度（％）",     // ラベル
                        fontColor: "black",             // 文字の色
                        fontSize: 16                    // フォントサイズ
                    },
                }]
            },
        },
    });
    return chart;
}


function makePieChart(colId, indexId, graphId, graphTitle) {
    // main
    const ctx = document.getElementById(graphId).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['国内債券', '国内株式', '先進国債券', '先進国株式'],
            datasets: [{
                backgroundColor: colorList.slice(0, 4),
                data: [0.35, 0.25, 0.15, 0.25],
            }],
        },
        options: {
            title: {
                display: true,
                text: graphTitle,
                padding: 5,
            },
            legend: {
                labels: {
                    boxWidth: 30,
                    padding: 20,
                },
                display: true,
            },
            tooltips: {
                mode: 'label',
            },
        },
    });
    return chart;
}
