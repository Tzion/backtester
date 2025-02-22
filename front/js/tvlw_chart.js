import { generateCandlestickData, readCSVData } from './candlestick_generator.js';

// Chart configuration with time scale options
const chart = LightweightCharts.createChart(
    document.getElementById('container'), 
    {
        timeScale: {
            timeVisible: true,
            secondsVisible: true, // Show seconds
            tickMarkFormatter: (time) => {
                // Custom formatter for timestamps
                const date = new Date(time * 1000);
                return date.toLocaleString('en-US', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                });
            }
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
