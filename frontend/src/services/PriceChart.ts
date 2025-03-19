import { createChart, IChartApi, CandlestickSeries, HistogramSeries, ISeriesApi, createSeriesMarkers } from 'lightweight-charts'
import { generateCandlestickData } from '../utils/candlestick-generator'

export class PriceChart {
  private chart: IChartApi | null = null
  private mainSeries: ISeriesApi<'Candlestick'> | null = null
  private volumeSeries: ISeriesApi<'Histogram'> | null = null
  

  constructor() { }

  initChart(container: HTMLElement) {
    if (!container) return null

    this.chart = createChart(container, {
      width: container.clientWidth,
      height: 500,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
    })

    this.mainSeries = this.chart.addSeries(CandlestickSeries, {
      priceFormat: {
        type: 'price',
        precision: 2,
        minMove: 0.01,
      },
    })

    this.volumeSeries = this.chart.addSeries(HistogramSeries, {
      color: '#26a69a',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    })

    if (this.volumeSeries) {
      this.volumeSeries.priceScale().applyOptions({
        scaleMargins: {
          top: 0.8,
          bottom: 0,
        },
      })
    }

    return this.chart
  }

  loadChart(symbol: string) {
    if (!this.mainSeries || !this.volumeSeries) return

    // In a real app, you would fetch data from API based on symbol
    const candleData = generateCandlestickData()

    const volumeData = candleData.map(item => ({
      time: item.time,
      value: Math.random() * 1000000, // Mock volume data
      color: item.close >= item.open ? '#26a69a' : '#ef5350'
    }))

    this.mainSeries.setData(candleData)
    this.volumeSeries.setData(volumeData)

    const candleToMark = this.mainSeries.data().slice(-5)[4]
    const marker = [{
      time: candleToMark.time,
      position: 'aboveBar',
      color: '#f68410',
      shape: 'circle',
      text: 'A',
    }]
    createSeriesMarkers(this.mainSeries, marker)
    this.chart?.timeScale().fitContent()
  }

  resize(width: number) {
    this.chart?.applyOptions({ width })
  }

  remove() {
    this.chart?.remove()
    this.chart = null
    this.mainSeries = null
    this.volumeSeries = null
  }
} 