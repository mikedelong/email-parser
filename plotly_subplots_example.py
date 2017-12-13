# https://plot.ly/python/subplots/

import plotly.graph_objs as graph_objs
import plotly.offline as offline
from plotly import tools

trace1 = graph_objs.Scatter(
    x=[1, 2, 3],
    y=[4, 5, 6]
)

trace2 = graph_objs.Scatter(
    x=[20, 30, 40],
    y=[50, 60, 70],
)

fig = tools.make_subplots(rows=1, cols=2)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)

fig['layout'].update(height=600, width=600, title='see subplots run')
offline.plot(fig, filename='simple-subplot.html')
