import { fetchOHLCV } from './data-fetcher.js';
import { createChart, createSeriesMarkers, CandlestickSeries, HistogramSeries } from 'lightweight-charts';

const chart = createChart(
    document.body,
    {
        timeScale: {
            timeVisible: true,
        },
        width: window.innerWeight,
        height: window.innerHeight
    }
);

let mainSeries;

async function renderChart(symbol) {
    try {
        const data = await fetchOHLCV(symbol);
        loadPrice(chart,data);

        const volumeData = data.map(item => ({
            time: item.time,
            value: item.volume
        }));
        loadVolume(chart, volumeData);
        createMarkers(chart);
        chart.timeScale().fitContent();
    } catch (error) {
        console.error(`Error rendering chart for symbol ${symbol}:`, error);
    }
}

function loadPrice(chart, priceData) {
    mainSeries = chart.addSeries(CandlestickSeries, {
        priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01
        }
    });

    mainSeries.setData(priceData);
}


function loadVolume(chart, volumeData) {
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
}

function createMarkers(chart) {
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

export { renderChart };

renderChart('SPY-1m');