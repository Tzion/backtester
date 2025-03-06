// Using native fetch API (preferred in Deno)
const API_BASE_URL = "http://localhost:8000";

export default {
  async listTrades() {
    const response = await fetch(`${API_BASE_URL}/trades`);
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
  },

  async getTradeDetails(tradeName: string) {
    const response = await fetch(`${API_BASE_URL}/trades/${tradeName}`);
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
  },

  async listObserverCharts() {
    const response = await fetch(`${API_BASE_URL}/observers`);
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
  },

  async getObserverChart(chartName: string) {
    const response = await fetch(`${API_BASE_URL}/observers/${chartName}`);
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return await response.json();
  }
}; 