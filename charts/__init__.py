import os

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS_DIR = os.path.join(BASE_DIR, "output", "charts")
TRADES_DIR = os.path.join(CHARTS_DIR, "trades")
OBSERVERS_DIR = os.path.join(CHARTS_DIR, "observers")

# Ensure directories exist
os.makedirs(TRADES_DIR, exist_ok=True)
os.makedirs(OBSERVERS_DIR, exist_ok=True)

''' put in this table attributes of mathplotlib need to be converted to plotly convention
    format is one of the follow:
    1. mathplotlib_key: plotly_key
    2. mathplotlib_key: (plotly_key, dict(mathplotlib_value: plotly_value))
    '''
MATHPLOTLIB_TO_PLOTLY_ATTRIBUTES = {
    'marker': ('marker_symbol', {
        'd': 'diamond',
        'o': 'circle',
        '*': 'star'
    }),
    'markersize': 'marker_size',
    'alpha': 'opacity',
    'markercolor': 'marker_color',
    'linewidth': 'line_width',
    'linecolor': 'line_color',
    'ls' : ('line_dash',
                        {'--': 'dash',
                        '-': 'solid',
                        ':': 'dot'}
                        ),
    
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

