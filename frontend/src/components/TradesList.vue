<template>
  <div class="trades-list">
    <div v-if="loading">Loading trades...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="trades-table">
      <thead>
        <tr>
          <th>Filename</th>
          <th>Size</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trade in trades" :key="trade.filename">
          <td>{{ trade.filename }}</td>
          <td>{{ formatSize(trade.size) }}</td>
          <td>{{ formatDate(trade.created) }}</td>
          <td>
            <button @click="viewTradeDetails(trade.filename)">View</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const trades = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    trades.value = await api.listTrades()
    loading.value = false
  } catch (err) {
    error.value = 'Failed to load trades'
    loading.value = false
  }
})

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

function formatDate(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString()
}

function viewTradeDetails(filename: string) {
  // Implement view details functionality
  console.log(`Viewing trade: ${filename}`)
}
</script>

<style scoped>
.trades-table {
  width: 100%;
  border-collapse: collapse;
}

.trades-table th, .trades-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.trades-table th {
  background-color: #f2f2f2;
}

.trades-table tr:hover {
  background-color: #f5f5f5;
}

button {
  padding: 4px 8px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style> 