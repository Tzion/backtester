from globals import *

class PartialLevel(bt.Indicator):
    lines = ('level',)
    plotlines = dict(level=dict(linewidth=9.0, ls=':'))
    plotinfo = dict(plot=True, subplot=False)

    def __init__(self, signal, level, length=10, color='deepskyblue'):
        self.signal = signal
        self.level = level
        self.length = length
        self.plotlines.level.color = color

    def once(self, start, end):
        for i in range(start,end):
            for j in range(i-self.length+1, i+1):
                if not math.isnan(self.signal[j]):
                    self.lines.level[i] = self.level[j]
                    break

class SingleMarker(bt.Indicator):
    lines = ('markers',)
    plotlines = dict(markers=dict(markersize=8.0,))
    plotinfo = dict(plot=False, subplot=False, plotlinelabels=True)
    
    def __init__(self, signals, level, marker='d', color='springgreen'):
        self.signals = signals
        self.level = level
        self.plotlines.markers.marker = marker
        self.plotlines.markers.color = color
        # TODO Potential bug with the left most value on the chart
        # self.addminperiod(1)

    def once(self, start, end):
        for i in range(start, end):
            if self.signals[i]:
                self.lines.markers[i] = self.level[i]
