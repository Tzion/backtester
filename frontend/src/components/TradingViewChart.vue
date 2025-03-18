<template>
  <div class="trading-view-chart">
    <div class="chart-controls">
      <select v-model="selectedSymbol" @change="handleSymbolChange">
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
import { PriceChart } from '@/services/PriceChart'

const chartContainer = ref<HTMLElement | null>(null)
const selectedSymbol = ref('SPY-1m')
const priceChart = new PriceChart()

onMounted(() => {
  if (chartContainer.value) {
    priceChart.initChart(chartContainer.value)
    priceChart.loadChart(selectedSymbol.value)
    
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  priceChart.remove()
  window.removeEventListener('resize', handleResize)
})

function handleSymbolChange() {
  priceChart.loadChart(selectedSymbol.value)
}

function handleResize() {
  if (chartContainer.value) {
    priceChart.resize(chartContainer.value.clientWidth)
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