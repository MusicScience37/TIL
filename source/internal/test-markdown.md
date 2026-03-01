---
file_format: mystnb
---

# マークダウンの動作確認

```{code-cell}
# 共通設定
import plotly.io
import ms37_designs.plotly_templates

plotly.io.renderers.default = "notebook_connected"
ms37_designs.plotly_templates.load_templates()
plotly.io.templates.default = "ms37_white"
```

```{code-cell}
import numpy
import plotly.express

x = numpy.linspace(0.0, 2.0, 101)
y = numpy.sin(x)
fig = plotly.express.line(
    x=x,
    y=y,
    labels={"x": "$x$", "y": "$y$"},
    title=r"$\text{Sample plot} \  y = \sin{x}$",
)
fig.show()
```

$$
\|\bm{a}\|^2 + \|\bm{b}\|^2 = \|\bm{c}\|^2
$$

```{note}
note のテスト
```

Sphinx の role のテスト： {math}`x`
