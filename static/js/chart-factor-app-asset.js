// asset cumulative return chart
let factorDecompCol = 'factor-decomp-col';
let factorDecompData = 'factor-decomp-data';
let factorDecompGraph = 'factor-decomp-graph';
let factorDecompTitle = '資産累積リターン';
const factorDecompChart = makeBarGraph(factorDecompCol, factorDecompData, factorDecompGraph, factorDecompTitle, 1);

// factor cumulative return chart
let factorCol = 'factor-index-col';
let factorData = 'factor-index-data';
let factorGraph = 'factor-index-graph';
let factorTitle = 'ファクター累積リターン';
const factorChart = makeLineGraph(factorCol, factorData, factorGraph, factorTitle, 1);

// asset cumulative return chart
let assetCol = 'asset-index-col';
let assetData = 'asset-index-data';
let assetGraph = 'asset-index-graph';
let assetTitle = '資産累積リターン';
const assetChart = makeLineGraph(assetCol, assetData, assetGraph, assetTitle, 2);
