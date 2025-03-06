import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'  // Adjust as needed

export default {
  async listTrades() {
    const response = await axios.get(`${API_BASE_URL}/trades`)
    return response.data
  },

  async getTradeDetails(tradeName: string) {
    const response = await axios.get(`${API_BASE_URL}/trades/${tradeName}`)
    return response.data
  },

  async listObserverCharts() {
    const response = await axios.get(`${API_BASE_URL}/observers`)
    return response.data
  },

  async getObserverChart(chartName: string) {
    const response = await axios.get(`${API_BASE_URL}/observers/${chartName}`)
    return response.data
  }
} 