import plotly.graph_objects as go
import pandas as pd
import tikzplotly


df = pd.read_csv("volumes.csv")
dfr = pd.read_csv("volumes_r.csv")

fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Nelt"], y=df["Volume"]*1e6, mode='lines+markers', name='Original mesh'))
fig.add_trace(go.Scatter(x=dfr["Nelt"], y=dfr["Volume"]*1e6, mode='lines+markers', name='Remeshed mesh'))

fig.update_layout(xaxis_title='Number of elements',
                  yaxis_title='Volume (mL)',
                  xaxis_type="log",
                  showlegend=True)

tikzplotly.save("volumes.tex", fig)
# fig.show()
