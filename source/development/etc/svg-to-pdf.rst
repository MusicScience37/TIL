コマンドによる SVG から PDF への変換
=============================================

Linux のコマンドを用いて SVG ファイルを PDF ファイルへ変換する方法を調査した結果、
うまくいった方法をメモする。

背景
-------------

.. cspell: ignore Inkscape

この調査をした元の目的は、
Python でグラフを生成するライブラリ
`Plotly <https://plotly.com/python/>`_
で描画したグラフを PDF 形式のベクター画像にして TeX のドキュメントに挿入することだった。
しかし、Plotly では PDF ファイルを正しく生成できなかったため、
PDF と同じくベクター画像の SVG ファイルを Plotly に出力させ、
その SVG ファイルを PDF ファイルへ変換することにした。

最初はソフトウェア
`Inkscape <https://inkscape.org/ja/>`_
を用いて手動で変換を行っていたが、
グラフを追加・変更するのが面倒な上に、
バイナリの PDF ファイルが Git の履歴に増えていくのを抑制したくなったため、
Plotly で SVG ファイルを生成して PDF ファイルへ変換するまでを全てコマンドで自動化することにした。

.. note::
    調査した結果完成したスクリプト：
    `numerical-analysis-note リポジトリの make_pdf_plot.py <https://gitlab.com/MusicScience37Projects/numerical-analysis/numerical-analysis-note/-/blob/23ed59e3baa9077ecb1a5b16c0082e02eac73b6e/num_anal_plots/make_pdf_plot.py>`_

svg2pdf の適用
--------------------

.. cspell: ignore svglib

Python パッケージ
`svglib <https://pypi.org/project/svglib/>`_
を用いて SVG ファイルを PDF ファイルへ変換する。

1. svglib のインストール

   Python パッケージ svglib をインストールする。

   .. code-block:: console

       $ pip3 install svglib

2. 適用

   svglib パッケージに含まれるコマンドラインツール svg2pdf を以下のように用いる。

   .. code-block:: console

       $ svg2pdf <SVGファイルパス> -o <PDFファイルの出力先のパス>

テキストのパスへの変換（オプション）
---------------------------------------

.. cspell: ignore Ghostscript pdfwrite

svg2pdf で生成される PDF ファイルでは
テキストがフォントの埋め込みもされていない状態で含まれるため、
PDF の表示が環境依存してしまう。
その問題を、PDF にフォントを埋め込むか、PDF 内のテキストをパスに変換することで解決する。
ここでは、
`Ghostscript <https://www.ghostscript.com/>`_
を用いてPDF 内のテキストをパスに変換する方法を記載する。

1. Ghostscript のインストール

   Ghostscript を単体でインストールする方法は調べていないため不明。
   私は
   `Island of TeX の texlive リポジトリ <https://gitlab.com/islandoftex/images/texlive>`_
   にて管理されている Docker イメージに含まれる Ghostscript を使用している。

2. 適用

   .. code-block:: console

       $ gs -dNoOutputFonts -sDEVICE=pdfwrite -o <変換後のPDFファイルの出力先パス> <入力となるPDFファイルのパス>

.. todo::
    現状はグラフの画像に使用しているだけのため
    テキストをパスに変換するという方法で困っていないが、
    フォントを埋め込む方法もそのうち必要になるかもしれない。
