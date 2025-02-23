import { fetchOHLCV } from './data-fetcher.js';
import { createChart, createSeriesMarkers, CandlestickSeries, HistogramSeries } from 'lightweight-charts';

const chart = createChart(
    document.body,
    {
        timeScale: {
            timeVisible: true,
        },
        width: window.innerWidth,
        height: window.innerHeight
    }
);


async function renderChart(symbol) {
    try {
        const data = await fetchOHLCV(symbol);
        const mainSeries = loadPrice(chart, data);

        const volumeData = data.map(item => ({
            time: item.time,
            value: item.volume
        }));
        loadVolume(chart, volumeData);
        // createMarkers_example(mainSeries);
        chart.timeScale().fitContent();
    } catch (error) {
        console.error(`Error rendering chart for symbol ${symbol}:`, error);
    }
}

function loadPrice(chart, priceData) {
    const mainSeries = chart.addSeries(CandlestickSeries, {
        priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01
        }
    });

    mainSeries.setData(priceData);
    return mainSeries;
}


function loadVolume(chart, volumeData) {
    // TODO: color bars in red and green
    const volumeSeries = chart.addSeries(HistogramSeries, {
        color: '#26a68c',
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

// for documentsion - will later use with proper data
function createMarkers_example(series) {
    const candleToMark = series.data().slice(-5)[4]
    const marker = [{
        time: candleToMark.time,
        position: 'aboveBar',
        color: '#f68410',
        shape: 'circle',
        text: 'A',
    }]
    const markers = createSeriesMarkers(series, marker)
}

export { renderChart };

// usage example
renderChart('SPY-1m');


// TODO: use this handler for lazy loader. newVisibleLogicalRange.from and .to are indexes of visible data array
// function myVisibleLogicalRangeChangeHandler(newVisibleLogicalRange) {
//     if (newVisibleLogicalRange === null) {
//         // handle null
//     }

//     // handle new logical range
// }

// chart.timeScale().subscribeVisibleLogicalRangeChange(myVisibleLogicalRangeChangeHandler);