// asset cumulative return chart
let portPieCol = 'asset-index-col';
let portPieWeight = 'port-weight';
let portPieGraph = 'port-weight-graph';
let portPieTitle = 'ポートフォリオウェイト';
const portPieChart = makePieChart(portPieCol, portPieWeight, portPieGraph, portPieTitle);


let weight = document.getElementById(portPieWeight).value
console.log(weight)
weight = extractColName(weight)
console.log(weight)
