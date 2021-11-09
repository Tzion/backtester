from globals import OUTPUT_DIR

CHARTS_DIR = OUTPUT_DIR + 'charts/'
TRADES_DIR = CHARTS_DIR + 'trades/'
OBSERVERS_DIR = CHARTS_DIR + 'observers/'



MATHPLOTLIB_TO_PLOTLY_ATTRIBUTES = {
    'marker': 'marker_symbol',
    'markersize': 'marker_size',
    'ls' : ('line_dash', {'--': 'dash'})
}

def translate(plotlib_key, plotlib_value) -> tuple:
    table = MATHPLOTLIB_TO_PLOTLY_ATTRIBUTES
    key = table.get(plotlib_key)
    if not key:
        return plotlib_key, plotlib_value
    if type(key) is tuple:
        value = key[1].get(plotlib_value) or plotlib_value
        key = key[0]
        return key, value
    else:
        return key, plotlib_value

