---
file_format: mystnb
---

# マークダウンの動作確認

```{code-cell}
import numpy
import plotly.express
import plotly.graph_objects

x = numpy.linspace(0.0, 2.0, 101)
y = numpy.sin(x)
fig = plotly.express.line(
    x=x,
    y=y,
    labels={"x": "$x$", "y": "$y$"},
    title=r"$\text{Sample plot} \  y = \sin{x}$",
)
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
