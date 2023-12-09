---
file_format: mystnb
---

# マークダウンの動作確認

```{code-cell}
import plotly.express
import plotly.graph_objects

fig = plotly.express.line(x=[1, 2, 3], y=[3, 5, 4])
fig.update_layout(height=500)
plotly.graph_objects.FigureWidget(fig)
```

$$
\|\bm{a}\|^2 + \|\bm{b}\|^2 = \|\bm{c}\|^2
$$

```{note}
note のテスト
```

Sphinx の role のテスト： {math}`x`
