ベクタ画像の出力
====================

VTK でベクタ画像を出力したときの設定をここにメモしておく。

古いソースコードをもとにしたため変数名はあまり整ってない。

.. code:: C++

    auto renderWindow = vtkSmartPointer<vtkRenderWindow>::New();

    // ウインドウへの描画（省略）

    auto pdfExporter = vtkSmartPointer<vtkGL2PSExporter>::New();
    pdfExporter->SetInput(renderWindow);
    pdfExporter->TextAsPathOn();                // テキストをパスにして保存
    pdfExporter->Write3DPropsAsRasterImageOn(); // 3Dの物体はラスタ画像に変換
    pdfExporter->SetFilePrefix("test");

    pdfExporter->CompressOn();          // 圧縮したラスタ画像で PDF を作成
    pdfExporter->SetFileFormatToPDF();
    pdfExporter->Write();

    pdfExporter->CompressOff();         // SVG はファイルが gzip 圧縮されるだけで
    pdfExporter->SetFileFormatToSVG();  // 圧縮の意味はあまりない。
    pdfExporter->Write();

.. note::
    `VTK のリファレンス <https://vtk.org/doc/nightly/html/classvtkGL2PSExporter.html>`_
    によると、
    ``Write3DPropsAsRasterImageOn()``
    は OpenGL2 バックエンドの環境だと指定しなくても良い。
    ウィンドウに描画する時点でラスタライズしてしまうからだという。

作成した画像の例を示す。

.. image:: vector_graphics_example.*

なお、上記は

.. code:: rst

    .. image:: vector_graphics_example.*

という拡張子を自動で選ばせる方法で表示している。
(`上記の表記のリファレンス <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images>`_)

VTK で SVG と PDF を出力しておき Sphinx に自動選択させれば、
HTML のビルドは SVG 画像を、PDF のビルドは PDF 画像を使うようにできる。
（PDF のビルドをしていないため活用できていないが。）
