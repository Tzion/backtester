import { generateCandlestickData, readCSVData } from './candlestick_generator.js';

// Function to generate a sample set of Candlestick datapoints
const chart = LightweightCharts.createChart(
    document.getElementById('container')
);

// Generate sample data to use within a candlestick series
const longData = await readCSVData('../../data_feeds/SPY-1m-5days.csv');
const candleStickData = generateCandlestickData();

// Create the Main Series (Candlesticks)
const mainSeries = chart.addSeries(LightweightCharts.CandlestickSeries);

// Set the data for the Main Series
mainSeries.setData(longData);

// Adding a window resize event handler to resize the chart when
// the window size changes.
// Note: for more advanced examples (when the chart doesn't fill the entire window)
// you may need to use ResizeObserver -> https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
// window.addEventListener("resize", () => {
//     chart.resize(window.innerWidth, window.innerHeight);
// });