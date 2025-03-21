import TradingViewChart from '../components/TradingViewChart.vue';

export default {
  title: 'Components/TradingViewChart',
  component: TradingViewChart,
  argTypes: {
    selectedSymbol: {
      control: 'select',
      options: ['SPY-1m', 'AAPL-1m'],
      description: 'The trading symbol to display'
    }
  },
};

export const Default = {
  render: (args) => ({
    components: { TradingViewChart },
    setup() {
      return { args };
    },
    template: '<TradingViewChart v-bind="args" />'
  }),
  args: {
    selectedSymbol: 'SPY-1m'
  }
};

// You can add more stories to show different states
export const WithCustomHeight = {
  render: (args) => ({
    components: { TradingViewChart },
    setup() {
      return { args };
    },
    template: '<div style="height: 800px;"><TradingViewChart v-bind="args" /></div>'
  }),
  args: {
    selectedSymbol: 'SPY-1m'
  }
};