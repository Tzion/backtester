import { generateCandlestickData, readCSVData } from './candlestick_generator.js';
import { createChart, createSeriesMarkers, CandlestickSeries, HistogramSeries } from 'lightweight-charts';
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
    const data = await readCSVData('../../data_feeds/SPY-1m.csv');
    // Split data into candlestick and volume arrays
    const ohlcData = data.map(item => ({
        time: item.time,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close
    }));

    const volumeData = data.map(item => ({
        time: item.time,
        value: item.volume
    }));

    // Create the Main Series (Candlesticks)
    const mainSeries = chart.addSeries(CandlestickSeries, {
        priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01
        }
    });

    mainSeries.setData(ohlcData);


    // test volume
    const volumeSeries = chart.addSeries(HistogramSeries, {
        color: '#26a69a',
        priceFormat: {
            type: 'volume',
        },
        priceScaleId: '', // set as an overlay by setting a blank priceScaleId
    });

    volumeSeries.priceScale().applyOptions({
        scaleMargins: {
            top: 0.4, // highest point of the series will be (0.X/1)% away from the top
            bottom: 0.0,
        },
    });
    volumeSeries.setData(volumeData);

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

    chart.timeScale().fitContent();


}

loadChartData();