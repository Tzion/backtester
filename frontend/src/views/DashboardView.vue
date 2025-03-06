<template>
  <div class="dashboard">
    <h1>Trading Dashboard</h1>
    
    <section class="observer-charts">
      <h2>Observer Charts</h2>
      <ObserverCharts />
    </section>
    
    <section class="trades-list">
      <h2>Trades</h2>
      <TradesList />
    </section>

    <section class="trading-view">
      <h2>Trading View</h2>
      <TradingViewChart />
    </section>
  </div>
</template>

<script setup lang="ts">
import ObserverCharts from '../components/ObserverCharts.vue'
import TradesList from '../components/TradesList.vue'
import TradingViewChart from '../components/TradingViewChart.vue'
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

section {
  margin-bottom: 30px;
}
</style> 