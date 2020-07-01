// data preparation
var graphLabel = [];
var colName = document.getElementById("indexCols").value;
var indexData = document.getElementById("indexData").value.split('\n');
const colorList = ['tomato', 'cornflowerblue', 'lightgreen', 'khaki', 'darkorange', 'hotpink', 'darkgoldenrod', 'darkred', 'slategray'];

// 
colName = colName.split('\'');
var id = [];
for (var i = 0; i < colName.length; i++) {
    if (colName[i].length > 2) {
        id.push(colName[i]);
    }
}
colName = id.slice(1);

indexData = indexData.slice(2);
for (var i = 0; i < indexData.length; i++) {
    graphLabel.push(indexData[i].split(' ')[0]);
    var id = [];
    var r = indexData[i].split(' ');
    for (var j = 0; j < r.length; j++) {
        if (r[j] !== '') {
            id.push(Number(r[j]));
        }
    }
    indexData[i] = id.slice(1);
}

// transpose data
const transpose = a => a[0].map((_, c) => a.map(r => r[c]));
indexData = transpose(indexData);

// set graph data
var allData = [];
for (var i = 0; i < indexData.length; i++) {
    allData.push({
        label: colName[i],
        borderColor: colorList[i],
        backgroundColor: colorList[i],
        borderWidth: 3,
        data: indexData[i],
        lineTension: 0,
        fill: false,
    });
}

// main
var ctxAsset = document.getElementById('index-graph').getContext('2d');
var chartAsset = new Chart(ctxAsset, {
    type: 'line',
    data: {
        labels: graphLabel,
        datasets: allData,
    },
    options: {
        title: {
            display: true,
            text: 'インデックス推移', //グラフの見出し
            padding: 5
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