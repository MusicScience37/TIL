# 閉じることのできるブロックを作成する

[sphinx-togglebutton](https://sphinx-togglebutton.readthedocs.io/en/latest/index.html)
を使用して閉じることの可能なブロックを作成する。

## インストール

```shell
pip3 install sphinx-togglebutton
```

## 設定

`conf.py` に以下の設定を追加する。

```python
extensions = [
    'sphinx_togglebutton',
]
```

## 使用方法

記述例：

````md
```{toggle}
サンプルコード
```
````

表示例：

```{toggle}
サンプルコード
```
