import { generateCandlestickData, readCSVData } from './candlestick_generator.js';
import { createChart, createSeriesMarkers, CandlestickSeries } from 'lightweight-charts';
// import LightweightCharts from 'lightweight-charts';

// Chart configuration with time scale options
const chart = createChart(
    document.getElementById('container'),
    {
        timeScale: {
            timeVisible: true,
        }
    }
);

async function loadChartData() {
    // Generate or load 1-minute chart data
    const longData = await readCSVData('../../data_feeds/SPY-1m.csv');

    // Create the Main Series (Candlesticks)
    const mainSeries = chart.addSeries(CandlestickSeries, {
        priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01
        }
    });

    mainSeries.setData(longData);
    chart.timeScale().fitContent();

    // test of markers
    const candleToMark = mainSeries.data().slice(-5)[4]
    const marker = [{
        time: candleToMark.time,
        position: 'aboveBar',
        color: '#f68410',
        shape: 'circle',
        text: 'A',
    }]
    const markers = createSeriesMarkers(mainSeries, marker)


}

loadChartData();