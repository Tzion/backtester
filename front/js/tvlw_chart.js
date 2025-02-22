import { generateCandlestickData, readCSVData } from './candlestick_generator.js';

// Chart configuration with time scale options
const chart = LightweightCharts.createChart(
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
    const mainSeries = chart.addSeries(LightweightCharts.CandlestickSeries, {
        priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01
        }
    });

    mainSeries.setData(longData);
    chart.timeScale().fitContent();
}

loadChartData();
