<template>
  <div class="trading-view-chart">
    <div class="chart-controls">
      <select v-model="selectedSymbol" @change="loadChart">
        <option value="SPY-1m">SPY (1m)</option>
        <option value="AAPL-1m">AAPL (1m)</option>
        <!-- Add more symbols as needed -->
      </select>
    </div>
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { createChart, CandlestickSeries, HistogramSeries } from 'lightweight-charts'
import { generateCandlestickData } from '../utils/candlestick-generator'

const chartContainer = ref(null)
const selectedSymbol = ref('SPY-1m')
let chart: any = null
let mainSeries: any = null
let volumeSeries: any = null

onMounted(() => {
  initChart()
  loadChart()
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (chart) {
    chart.remove()
    chart = null
  }
  window.removeEventListener('resize', handleResize)
})

function initChart() {
  if (!chartContainer.value) return
  
  chart = createChart(chartContainer.value, {
    width: chartContainer.value.clientWidth,
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
  
  mainSeries = chart.addSeries({
    type: 'Candlestick',
    priceFormat: {
      type: 'price',
      precision: 2,
      minMove: 0.01,
    },
  })
  
  volumeSeries = chart.addSeries({
    type: 'Histogram',
    color: '#26a69a',
    priceFormat: {
      type: 'volume',
    },
    priceScaleId: '',
  })
  
  volumeSeries.priceScale().applyOptions({
    scaleMargins: {
      top: 0.8,
      bottom: 0,
    },
  })
}

function loadChart() {
  if (!mainSeries || !volumeSeries) return
  
  // In a real app, you would fetch data from API based on selectedSymbol
  const candleData = generateCandlestickData()
  
  const volumeData = candleData.map(item => ({
    time: item.time,
    value: Math.random() * 1000000, // Mock volume data
    color: item.close >= item.open ? '#26a69a' : '#ef5350'
  }))
  
  mainSeries.setData(candleData)
  volumeSeries.setData(volumeData)
  
  chart.timeScale().fitContent()
}

function handleResize() {
  if (chart && chartContainer.value) {
    chart.applyOptions({
      width: chartContainer.value.clientWidth,
    })
  }
}
</script>

<style scoped>
.trading-view-chart {
  width: 100%;
}

.chart-controls {
  margin-bottom: 10px;
}

.chart-controls select {
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.chart-container {
  width: 100%;
  height: 500px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style> 