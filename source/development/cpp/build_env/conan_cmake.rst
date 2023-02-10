.. _development-cpp-conan_cmake:

Conan を用いた CMake の依存ライブラリ管理
=============================================

..
    cspell:ignore helloworld conanfile conans conanmanifest conaninfo
    cspell:ignore RPATHs arenastring lited libprotobufd libprotocd protoc proto
    cspell:ignore graphinfo protocd protobufd

`Conan <https://conan.io/>`_
は C/C++ 向けのパッケージマネージャで、
プロジェクトごとの設定ファイルに書かれた通りに依存ライブラリをインストールできるほか、
パッケージを作成することもできる。
パッケージをインストールするもとになるサーバを選択可能な分散型のシステムとなっており、
非公開のサーバを用意することができるほか、
公式の `Conan Center <https://conan.io/center/>`_ に様々な有名なライブラリのバイナリが用意されている。

インストールしたパッケージを使用できるようにするために必要なファイルを生成する
Generator には様々な種類が存在し、
CMake, Visual Studio, QMake など様々なビルド環境で使用できる
（ `Generators — conan 1.35.2 documentation <https://docs.conan.io/en/latest/reference/generators.html>`_ ）。

ここでは、CMake で使用することを前提として導入方法について検討する。

Conan のインストール
-----------------------

Conan のクライアントは Python で書かれており、
PyPi リポジトリに conan という名前で登録されている。
つまり、Python と pip がインストールされた環境であれば、
``pip install conan`` でインストールできる。

公式のインストール手順
（`Install — conan 1.35.2 documentation <https://docs.conan.io/en/latest/installation.html>`_）
では仮想環境の利用を強く推奨しているため、
今回は `pipenv <https://pipenv.pypa.io/en/latest/>`_ を使用してインストールした。
（:ref:`pipenv のメモ <development-python-pipenv>`）

CMake 向けの Generator
----------------------------

2021/4/25 現在、
CMake 向けの Generator には次のようなものがある
（参考、例の引用元：`CMake — conan 1.35.2 documentation <https://docs.conan.io/en/latest/integrations/build_system/cmake.html>`_）。

``cmake`` generator
    ``cmake`` generator を選択すると、
    conanbuildinfo.cmake というファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup(TARGETS)

        add_executable(timer timer.cpp)
        target_link_libraries(timer CONAN_PKG::poco)

``cmake_multi`` generator
    ``cmake_multi`` generator を選択すると、
    ``cmake`` generator と同様の CMakefile.txt で
    CMake の multi-configuration
    （Visual Studio のように Debug や Release のビルドをまとめて行うこと）
    に対応できる。

``cmake_paths`` generator
    ``cmake_paths`` generator を選択すると、
    conan_paths.cmake というファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        cmake_minimum_required(VERSION 3.0)
        project(helloworld)

        include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

        add_executable(helloworld hello.c)

        find_package(zlib)

        if(ZLIB_FOUND)
           include_directories(${ZLIB_INCLUDE_DIRS})
           target_link_libraries (helloworld ${ZLIB_LIBRARIES})
        endif()

``cmake_find_package`` generator
    ``cmake_find_package`` generator を選択すると、
    ``Find<パッケージ名>.cmake`` の形式のファイルが生成され、
    CMakefile.txt から次のようにインストールされたパッケージを読み込むことができる。

    .. code-block:: cmake

        cmake_minimum_required(VERSION 3.0)
        project(helloworld)
        # Conan が生成したファイルを正しく使用できるようにパスを追加
        list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
        list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

        add_executable(helloworld hello.c)
        find_package(ZLIB)

        # Global approach
        if(ZLIB_FOUND)
           include_directories(${ZLIB_INCLUDE_DIRS})
           target_link_libraries (helloworld ${ZLIB_LIBRARIES})
        endif()

        # Modern CMake targets approach
        if(TARGET ZLIB::ZLIB)
           target_link_libraries(helloworld ZLIB::ZLIB)
        endif()

``cmake_find_package_multi`` generator
    ``cmake_find_package_multi`` generator は
    ``cmake_find_package`` generator を
    CMake の multi-configuration に対応させたもの。

CMakefile.txt が Conan に直接依存しない ``cmake_find_package`` generator は、
比較的容易に Conan を試すことができて良いのではないだろうか。

設定ファイル
---------------------

Conan 用の設定ファイルには次の 2 種類があり、
プロジェクトごとにいずれかの設定ファイルが必要となる。

conanfile.txt
    シンプルな設定ファイル

    .. code-block:: text

        [requires]
        poco/1.9.4
        zlib/1.2.11

        [generators]
        cmake

conanfile.py
    Python のスクリプトでクラスとして書く設定ファイル

    .. code-block:: python

        from conans import ConanFile

        class ExampleConan(ConanFile):
            requires = ("poco/1.9.4", "zlib/1.2.11")
            generators = "cmake"

conanfile.py の方が様々な設定を行うことができ、
特にパッケージを作成する場合は conanfile.py が必要となる。
conanfile.py の詳細は
`conanfile.py — conan 1.35.2 documentation <https://docs.conan.io/en/latest/reference/conanfile.html>`_
を参照。

パッケージのインストール
-----------------------------------

conanfile.txt または conanfile.txt を作成すると、
``conan install`` コマンドで requires に指定したパッケージをインストールできる。

ここでは、次のような conanfile.py を用意した。

.. code-block:: py

    from conans import ConanFile, CMake


    class TestConan(ConanFile):
        requires = "protobuf/3.15.5"
        generators = "cmake_find_package"

.. note::
    本ページにおける動作確認を行ったリポジトリ：
    `test_conan_20210425 <https://gitlab.com/MusicScience37/test_conan_20210425>`_

CMake と同様にビルドディレクトリを作成し、
ビルドディレクトリから ``conan install`` コマンドを起動し、
オプションとして conanfile.py のあるディレクトリを指定することで、
パッケージのインストールを行う。

.. code-block:: console

    $ cd path/to/project
    $ mkdir -p build/Debug
    $ cd build/Debug
    $ pipenv run conan install -s compiler=clang -s compiler.version=11 -e CC=clang -e CXX=clang++ --build=missing -s build_type=Debug ../..
    Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
    Auto detecting your dev setup to initialize the default profile (/home/kenta/.conan/profiles/default)
    Found gcc 9
    Found clang 11.0
    gcc>=5, using the major as version

    ************************* WARNING: GCC OLD ABI COMPATIBILITY ***********************

    Conan detected a GCC version > 5 but has adjusted the 'compiler.libcxx' setting to
    'libstdc++' for backwards compatibility.
    Your compiler is likely using the new CXX11 ABI by default (libstdc++11).

    If you want Conan to use the new ABI for the default profile, run:

        $ conan profile update settings.compiler.libcxx=libstdc++11 default

    Or edit '/home/kenta/.conan/profiles/default' and set compiler.libcxx=libstdc++11

    ************************************************************************************



    Default settings
            os=Linux
            os_build=Linux
            arch=x86_64
            arch_build=x86_64
            compiler=gcc
            compiler.version=9
            compiler.libcxx=libstdc++
            build_type=Release
    *** You can change them in /home/kenta/.conan/profiles/default ***
    *** Or override with -s compiler='other' -s ...s***


    WARN: Remotes registry file missing, creating default one in /home/kenta/.conan/remotes.json
    Configuration:
    [settings]
    arch=x86_64
    arch_build=x86_64
    build_type=Debug
    compiler=clang
    compiler.version=11
    os=Linux
    os_build=Linux
    [options]
    [build_requires]
    [env]
    CC=clang
    CXX=clang++
    protobuf/3.15.5: Not found in local cache, looking in remotes...
    protobuf/3.15.5: Trying with 'conan-center'...
    Downloading conanmanifest.txt completed [0.55k]
    Downloading conanfile.py completed [12.57k]
    Downloading conan_export.tgz completed [0.31k]
    Decompressing conan_export.tgz completed [0.00k]
    protobuf/3.15.5: Downloaded recipe revision 0
    zlib/1.2.11: Not found in local cache, looking in remotes...
    zlib/1.2.11: Trying with 'conan-center'...
    Downloading conanmanifest.txt completed [0.35k]
    Downloading conanfile.py completed [5.95k]
    Downloading conan_export.tgz completed [0.34k]
    Decompressing conan_export.tgz completed [0.00k]
    zlib/1.2.11: Downloaded recipe revision 0
    conanfile.py: Installing package
    Requirements
        protobuf/3.15.5 from 'conan-center' - Downloaded
        zlib/1.2.11 from 'conan-center' - Downloaded
    Packages
        protobuf/3.15.5:23876dd24f3c2d15c60cbb682812eb05c5bbe168 - Build
        zlib/1.2.11:05441c20e7e7a68951563eb6a1ae544f71dd7263 - Download

    Installing (downloading, building) binaries...
    zlib/1.2.11: Retrieving package 05441c20e7e7a68951563eb6a1ae544f71dd7263 from remote 'conan-center'
    Downloading conanmanifest.txt completed [0.25k]
    Downloading conaninfo.txt completed [0.41k]
    Downloading conan_package.tgz completed [137.50k]
    Decompressing conan_package.tgz completed [0.00k]
    zlib/1.2.11: Package installed 05441c20e7e7a68951563eb6a1ae544f71dd7263
    zlib/1.2.11: Downloaded package revision 0
    Downloading conan_sources.tgz completed [1.82k]
    Decompressing conan_sources.tgz completed [0.00k]
    protobuf/3.15.5: Configuring sources in /home/kenta/.conan/data/protobuf/3.15.5/_/_/source
    Downloading v3.15.5.tar.gz completed [5159.88k]

    protobuf/3.15.5: Copying sources to build folder
    protobuf/3.15.5: Building your package in /home/kenta/.conan/data/protobuf/3.15.5/_/_/build/23876dd24f3c2d15c60cbb682812eb05c5bbe168
    protobuf/3.15.5: Generator cmake created conanbuildinfo.cmake
    protobuf/3.15.5: Calling build()
    -- The C compiler identification is Clang 11.0.0
    -- The CXX compiler identification is Clang 11.0.0
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working C compiler: /home/kenta/programs/llvm/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04/bin/clang - skipped
    -- Detecting C compile features
    -- Detecting C compile features - done
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Check for working CXX compiler: /home/kenta/programs/llvm/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04/bin/clang++ - skipped
    -- Detecting CXX compile features
    -- Detecting CXX compile features - done
    -- Conan: called by CMake conan helper
    -- Conan: called inside local cache
    -- Conan: Adjusting output directories
    -- Conan: Using cmake targets configuration
    -- Library z found /home/kenta/.conan/data/zlib/1.2.11/_/_/package/05441c20e7e7a68951563eb6a1ae544f71dd7263/lib/libz.a
    -- Conan: Adjusting default RPATHs Conan policies
    -- Conan: Adjusting language standard
    -- Conan: Adjusting fPIC flag (ON)
    -- Conan: Compiler Clang>=8, checking major version 11
    -- Conan: Checking correct version: 11
    --
    -- 3.15.5.0
    -- Looking for pthread.h
    -- Looking for pthread.h - found
    -- Performing Test CMAKE_HAVE_LIBC_PTHREAD
    -- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
    -- Looking for pthread_create in pthreads
    -- Looking for pthread_create in pthreads - not found
    -- Looking for pthread_create in pthread
    -- Looking for pthread_create in pthread - found
    -- Found Threads: TRUE
    -- Found ZLIB: /home/kenta/.conan/data/zlib/1.2.11/_/_/package/05441c20e7e7a68951563eb6a1ae544f71dd7263/lib/libz.a (found version "1.2.11")
    -- Performing Test protobuf_HAVE_BUILTIN_ATOMICS
    -- Performing Test protobuf_HAVE_BUILTIN_ATOMICS - Success
    -- Configuring done
    -- Generating done
    CMake Warning:
      Manually-specified variables were not used by the project:

        CMAKE_EXPORT_NO_PACKAGE_REGISTRY


    -- Build files have been written to: /home/kenta/.conan/data/protobuf/3.15.5/_/_/build/23876dd24f3c2d15c60cbb682812eb05c5bbe168/build_subfolder
    [  1%] Building CXX object source_subfolder/cmake/CMakeFiles/libprotobuf-lite.dir/__/src/google/protobuf/any_lite.cc.o
    [  1%] Building CXX object source_subfolder/cmake/CMakeFiles/libprotobuf-lite.dir/__/src/google/protobuf/arena.cc.o
    [  2%] Building CXX object source_subfolder/cmake/CMakeFiles/libprotobuf-lite.dir/__/src/google/protobuf/arenastring.cc.o
    [  3%] Building CXX object source_subfolder/cmake/CMakeFiles/libprotobuf-lite.dir/__/src/google/protobuf/generated_message_table_driven_lite.cc.o

    （中略）

    -- Installing: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/cmake/protobuf/protobuf-config.cmake
    -- Installing: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/cmake/protobuf/protobuf-options.cmake
    -- Installing: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/cmake/protobuf/protobuf-config-version.cmake
    -- Installing: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/cmake/protobuf/protobuf-module.cmake
    protobuf/3.15.5 package(): Packaged 3 '.a' files: libprotobuf-lited.a, libprotobufd.a, libprotocd.a
    protobuf/3.15.5 package(): Packaged 3 '.cmake' files: protobuf-generate.cmake, protobuf-options.cmake, protobuf-module.cmake
    protobuf/3.15.5 package(): Packaged 2 files: LICENSE, protoc
    protobuf/3.15.5 package(): Packaged 1 '.0' file: protoc-3.15.5.0
    protobuf/3.15.5 package(): Packaged 100 '.h' files
    protobuf/3.15.5 package(): Packaged 12 '.proto' files
    protobuf/3.15.5 package(): Packaged 2 '.inc' files: port_undef.inc, port_def.inc
    protobuf/3.15.5: Package '23876dd24f3c2d15c60cbb682812eb05c5bbe168' created
    protobuf/3.15.5: Created package revision 44c662db43db36600fea6f57ded52561
    protobuf/3.15.5: Appending PATH environment variable: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/bin
    conanfile.py: Generator cmake_find_package created FindProtobuf.cmake
    conanfile.py: Generator cmake_find_package created FindZLIB.cmake
    conanfile.py: Generator txt created conanbuildinfo.txt
    conanfile.py: Generated conaninfo.txt
    conanfile.py: Generated graphinfo

.. note::
    Conan を pipenv でインストールしたため、
    pipenv を通して conan コマンドを使用している。

.. note::
    ``-s compiler=clang -s compiler.version=11`` のように
    オプションでコンパイラが指定できる。
    バージョンまで指定しなければ実行時にエラーが発生する。
    さらに、Conan Center にバイナリがないパッケージにおいては
    CMake コマンドによるビルドを行うため、
    CC, CXX 環境変数も必要。

.. note::
    Debug / Release を指定するには ``-s build_type=Debug`` のようなオプション指定が必要。

以上でインストールが完了する。
なお、インストールされたパッケージはプロジェクトのディレクトリとは別の
``~/.conan`` ディレクトリ配下に置かれるため、
プロジェクト間で共有できる。

インストールしたパッケージの使用
-----------------------------------

protobuf を用いた CMakefile.txt は次のようになる。

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.12)

    project(
        test_conan
        VERSION 0.0.0
        DESCRIPTION "test of conan for C++ project"
        LANGUAGES CXX)
    message(STATUS "test_conan")
    message(STATUS "build type: ${CMAKE_BUILD_TYPE}")

    # Conan が生成した FindProtobuf.cmake は ${CMAKE_BINARY_DIR} にあるため
    # ${CMAKE_BINARY_DIR} をパスへ追加する。
    list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
    list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

    # Conan が生成した FindProtobuf.cmake を読み込む。
    find_package(Protobuf REQUIRED)
    set(GENERATED_SOURCE_DIR ${CMAKE_BINARY_DIR}/generated)
    set(MESSAGE_PROTO ${CMAKE_CURRENT_SOURCE_DIR}/test_messages.proto)
    set(MESSAGE_SOURCE ${GENERATED_SOURCE_DIR}/test_messages.pb.cc)
    # FindProtobuf.cmake が追加する protobuf::protoc ターゲットを使用する。
    add_custom_command(
        OUTPUT ${MESSAGE_SOURCE}
        COMMAND protobuf::protoc --cpp_out ${GENERATED_SOURCE_DIR} --proto_path
                ${CMAKE_CURRENT_SOURCE_DIR} ${MESSAGE_PROTO}
        DEPENDS ${MESSAGE_PROTO} protobuf::protoc)

    add_executable(test_protobuf test_main.cpp ${MESSAGE_SOURCE})
    target_include_directories(test_protobuf PRIVATE ${GENERATED_SOURCE_DIR})
    # FindProtobuf.cmake が追加する protobuf::protobuf ターゲットを使用する。
    target_link_libraries(test_protobuf PRIVATE protobuf::protobuf)

CMakefile.txt については以下を参照した。

- `Serializing your data with Protobuf <https://blog.conan.io/2019/03/06/Serializing-your-data-with-Protobuf.html>`_
- `FindProtobuf — CMake 3.20.1 Documentation <https://cmake.org/cmake/help/latest/module/FindProtobuf.html>`_
- `add_custom_command — CMake 3.20.1 Documentation <https://cmake.org/cmake/help/latest/command/add_custom_command.html>`_

.. note::
    protoc の出力先を指定するには、
    FindProtobuf.cmake が追加する protobuf_generate_cpp 関数に頼らず
    自力で add_custom_command 関数を書く必要がある。

Conan のパッケージのライブラリが使用されていることは、
CMake の configure を行う際のログで確認できる。

.. code-block:: text

    Not searching for unused variables given on the command line.
    -- The CXX compiler identification is Clang 11.0.0
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Check for working CXX compiler: /home/kenta/programs/llvm/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04/bin/clang++ - skipped
    -- Detecting CXX compile features
    -- Detecting CXX compile features - done
    -- test_conan
    -- build type: Debug
    -- Conan: Using autogenerated FindProtobuf.cmake
    -- Found Protobuf: 3.15.5 (found version "3.15.5")
    -- Library protocd found /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotocd.a
    -- Found: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotocd.a
    -- Library protobufd found /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotobufd.a
    -- Found: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotobufd.a
    -- Conan: Using autogenerated FindZLIB.cmake
    -- Found ZLIB: 1.2.11 (found version "1.2.11")
    -- Library z found /home/kenta/.conan/data/zlib/1.2.11/_/_/package/05441c20e7e7a68951563eb6a1ae544f71dd7263/lib/libz.a
    -- Found: /home/kenta/.conan/data/zlib/1.2.11/_/_/package/05441c20e7e7a68951563eb6a1ae544f71dd7263/lib/libz.a
    -- Library protobufd found /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotobufd.a
    -- Found: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotobufd.a
    -- Library protocd found /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotocd.a
    -- Found: /home/kenta/.conan/data/protobuf/3.15.5/_/_/package/23876dd24f3c2d15c60cbb682812eb05c5bbe168/lib/libprotocd.a
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/kenta/projects/test/test_conan_20210425/build/Debug

Git の submodule との比較
--------------------------------

- 導入は Git の submodule の方が簡単だった。
- Git の submodule と異なり、
  Conan は依存ライブラリをプロジェクト共通の場所に保存できるため、
  何度も同じ依存ライブラリをビルドする必要がない。
