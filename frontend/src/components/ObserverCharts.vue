<template>
  <div class="observer-charts">
    <div v-if="loading">Loading charts...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="chart-grid">
      <div v-for="chart in charts" :key="chart.filename" class="chart-item">
        <iframe 
          :src="`http://localhost:8000/observers/${chart.filename}`" 
          width="100%" 
          height="400px"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const charts = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    charts.value = await api.listObserverCharts()
    loading.value = false
  } catch (err) {
    error.value = 'Failed to load charts'
    loading.value = false
  }
})
</script>

<style scoped>
.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(600px, 1fr));
  gap: 20px;
}

.chart-item {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}
</style> 