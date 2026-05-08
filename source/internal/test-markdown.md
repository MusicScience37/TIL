---
file_format: mystnb
---

# マークダウンの動作確認

```{code-cell}
from til_utils.plot_common import load_common_config

load_common_config()
```

```{code-cell}
import numpy
import plotly.express
from til_utils.plot_common import show_figure

x = numpy.linspace(0.0, 2.0, 101)
y = numpy.sin(x)
fig = plotly.express.line(
    x=x,
    y=y,
    labels={"x": "$x$", "y": "$y$"},
    title=r"$\text{Sample plot} \  y = \sin{x}$",
)
show_figure(fig)
```

$$
\|\bm{a}\|^2 + \|\bm{b}\|^2 = \|\bm{c}\|^2
$$

```{note}
note のテスト
```

Sphinx の role のテスト： {math}`x`
