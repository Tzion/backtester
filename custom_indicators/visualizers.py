from globals import *

class PartialLevel(bt.Indicator):
    lines = ('level',)
    plotlines = dict(level=dict(linewidth=2, ls=':'))
    plotinfo = dict(plot=True, subplot=False)

    def __init__(self, signal, level, length=10, color='deepskyblue'):
        self.signal = signal
        self.level = level
        self.length = length
        self.plotlines.level.linecolor = color

    def once(self, start, end):
        for i in range(start,end):
            for j in range(i-self.length+1, i+1):
                if not math.isnan(self.signal[j]) and self.signal[j] != 0:
                    self.lines.level[i] = self.level[j]
                    break


class SingleMarker(bt.Indicator):  # For backward compatibility with bokeh
    lines = ('marker',)
    plotinfo = dict(plot=True, subplot=False, plotlinelabels=True)
    # plotlines = dict(markers=dict())
    
    def __init__(self, signals, level, marker='d', color='springgreen', markersize=8.0):
        self.signals = signals
        self.level = level
        self.plotlines.marker.marker = marker
        self.plotlines.marker.markercolor = color
        self.plotlines.marker.markersize = markersize
        self.plotlines.marker.mode = 'markers'

    def once(self, start, end):
        for i in range(start, end):
            if self.signals[i] != 0 and not math.isnan(self.signals[i]):
                self.lines.marker[i] = self.level[i]

