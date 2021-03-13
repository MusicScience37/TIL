ファイルの内容をすべて読み込む
===================================

C++ でファイルの内容をすべて読み込む処理をしばしば書くため、
簡単な処理方法をメモしておく。

.. code-block:: cpp

    #include <string>
    #include <fstream>
    #include <streambuf>

    std::ifstream stream(filepath);
    if (!stream) {
        // 開けなかったエラー通知
    }
    const auto contents = std::string(
        std::istreambuf_iterator<char>(stream),
        std::istreambuf_iterator<char>());

当然このソースコードではファイルの内容を全てメモリ上に展開するため、
重いファイルに使用しないように注意。

出展：
`Read whole ASCII file into C++ std::string - Stack Overflow <https://stackoverflow.com/questions/2602013/read-whole-ascii-file-into-c-stdstring>`_
