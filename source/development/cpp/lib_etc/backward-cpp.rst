.. _development-cpp-backward-cpp:

backward-cpp ライブラリ
===========================

`backward-cpp <https://github.com/bombela/backward-cpp>`_
は簡単に読みやすいスタックトレースを出力するライブラリ。

以下に使用してみた例を示す。

.. note::

    `このリポジトリ <https://gitlab.com/MusicScience37/test-backward-cpp>`_
    にソースコードとビルド用の CMakeLists.txt などを置いた。

スタックトレースを取得する例
----------------------------------

.. code-block:: cpp

    #include <backward.hpp>

    void test1() {
        backward::StackTrace st;
        st.load_here();
        backward::Printer p;
        p.object = true;
        p.color_mode = backward::ColorMode::automatic;
        p.address = true;
        p.print(st, stderr);
    }

    class Test {
    public:
        void test2(const std::string &) { test1(); }
    };

    int main() {
        Test().test2("abc");
        return 0;
    }

これを実行すると次のようになった。

.. code-block:: console

    $ ./bin/test_backtrace
    Stack trace (most recent call last):
    #7    Object "", at 0xffffffffffffffff, in
    #6    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x4048fd, in _start
    #5    Object "/lib/x86_64-linux-gnu/libc.so.6", at 0x7f820fff30b2, in __libc_start_main
    #4    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x404adf, in main
          Source "/home/kenta/test/test-backward-cpp/src/test_backtrace.cpp", line 19, in int main() [0x404adf]
             16: };
             17:
             18: int main() {
          >  19:     Test().test2("abc");
             20:     return 0;
             21: }
    #3    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x404e54, in Test::test2(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
          Source "/home/kenta/test/test-backward-cpp/src/test_backtrace.cpp", line 15, in Test::test2(const string &) [0x404e54]
             13: class Test {
             14: public:
          >  15:     void test2(const std::string &) { test1(); }
             16: };
             17:
             18: int main() {
    #2    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x4049f2, in test1()
          Source "/home/kenta/test/test-backward-cpp/src/test_backtrace.cpp", line 5, in test1() [0x4049f2]
              3: void test1() {
              4:     backward::StackTrace st;
          >   5:     st.load_here();
              6:     backward::Printer p;
              7:     p.object = true;
              8:     p.color_mode = backward::ColorMode::automatic;
    #1    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x404be1, in backward::StackTraceImpl<backward::system_tag::linux_tag>::load_here(unsigned long, void*, void*)
          Source "/home/kenta/.conan/data/backward-cpp/1.6/_/_/package/759153e8b6a68049c52431bd581c49bae41f8bda/include/backward.hpp", line 869, in size_t backward::StackTraceImpl<backward::system_tag::linux_tag>::load_here(size_t depth, void *context, void *error_addr) [0x404be1]
            866:       return 0;
            867:     }
            868:     _stacktrace.resize(depth);
          > 869:     size_t trace_cnt = details::unwind(callback(*this), depth);
            870:     _stacktrace.resize(trace_cnt);
            871:     skip_n_firsts(0);
            872:     return size();
    #0    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_backtrace", at 0x405110, in unsigned long backward::details::unwind<backward::StackTraceImpl<backward::system_tag::linux_tag>::callback>(backward::StackTraceImpl<backward::system_tag::linux_tag>::callback, unsigned long)
          Source "/home/kenta/.conan/data/backward-cpp/1.6/_/_/package/759153e8b6a68049c52431bd581c49bae41f8bda/include/backward.hpp", line 851, in size_t backward::details::unwind<backward::StackTraceImpl<backward::system_tag::linux_tag>::callback>(callback f, size_t depth) [0x405110]
            849: template <typename F> size_t unwind(F f, size_t depth) {
            850:   Unwinder<F> unwinder;
          > 851:   return unwinder(f, depth);
            852: }
            853:
            854: } // namespace details

例外にスタックトレースを含める例
-------------------------------------

.. code-block:: cpp

    #include <sstream>

    #include <backward.hpp>

    [[noreturn]] void throw_with_backtrace(const std::string& message) {
        std::ostringstream stream;
        stream << message << "\n\n";

        backward::StackTrace st;
        st.load_here();
        backward::Printer p;
        p.object = true;
        p.color_mode = backward::ColorMode::never;
        p.address = true;
        p.print(st, stream);

        throw std::runtime_error(stream.str());
    }

    void test1() { throw_with_backtrace("Test exception"); }

    class Test {
    public:
        void test2(const std::string&) { test1(); }
    };

    int main() {
        Test().test2("abc");
        return 0;
    }

これを実行すると次のようになった。

.. code-block:: console

    $ ./bin/test_exception
    terminate called after throwing an instance of 'std::runtime_error'
      what():  Test exception

    Stack trace (most recent call last):
    #8    Object "", at 0xffffffffffffffff, in
    #7    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x40381d, in _start
    #6    Object "/lib/x86_64-linux-gnu/libc.so.6", at 0x7f7b48a790b2, in __libc_start_main
    #5    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x403bbf, in main
          Source "/home/kenta/test/test-backward-cpp/src/test_exception.cpp", line 28, in int main() [0x403bbf]
             25: };
             26:
             27: int main() {
          >  28:     Test().test2("abc");
             29:     return 0;
             30: }
    #4    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x403e74, in Test::test2(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
          Source "/home/kenta/test/test-backward-cpp/src/test_exception.cpp", line 24, in Test::test2(const string &) [0x403e74]
             22: class Test {
             23: public:
          >  24:     void test2(const std::string&) { test1(); }
             25: };
             26:
             27: int main() {
    #3    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x403b34, in test1()
          Source "/home/kenta/test/test-backward-cpp/src/test_exception.cpp", line 20, in test1() [0x403b34]
             17:     throw std::runtime_error(stream.str());
             18: }
             19:
          >  20: void test1() { throw_with_backtrace("Test exception"); }
             21:
             22: class Test {
             23: public:
    #2    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x40395f, in throw_with_backtrace(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)
          Source "/home/kenta/test/test-backward-cpp/src/test_exception.cpp", line 10, in throw_with_backtrace(const string &message) [0x40395f]
              7:     stream << message << "\n\n";
              8:
              9:     backward::StackTrace st;
          >  10:     st.load_here();
             11:     backward::Printer p;
             12:     p.object = true;
             13:     p.color_mode = backward::ColorMode::never;
    #1    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x403cc1, in backward::StackTraceImpl<backward::system_tag::linux_tag>::load_here(unsigned long, void*, void*)
          Source "/home/kenta/.conan/data/backward-cpp/1.6/_/_/package/759153e8b6a68049c52431bd581c49bae41f8bda/include/backward.hpp", line 869, in size_t backward::StackTraceImpl<backward::system_tag::linux_tag>::load_here(size_t depth, void *context, void *error_addr) [0x403cc1]
            866:       return 0;
            867:     }
            868:     _stacktrace.resize(depth);
          > 869:     size_t trace_cnt = details::unwind(callback(*this), depth);
            870:     _stacktrace.resize(trace_cnt);
            871:     skip_n_firsts(0);
            872:     return size();
    #0    Object "/home/kenta/test/test-backward-cpp/build/Debug/bin/test_exception", at 0x404130, in unsigned long backward::details::unwind<backward::StackTraceImpl<backward::system_tag::linux_tag>::callback>(backward::StackTraceImpl<backward::system_tag::linux_tag>::callback, unsigned long)
          Source "/home/kenta/.conan/data/backward-cpp/1.6/_/_/package/759153e8b6a68049c52431bd581c49bae41f8bda/include/backward.hpp", line 851, in size_t backward::details::unwind<backward::StackTraceImpl<backward::system_tag::linux_tag>::callback>(callback f, size_t depth) [0x404130]
            849: template <typename F> size_t unwind(F f, size_t depth) {
            850:   Unwinder<F> unwinder;
          > 851:   return unwinder(f, depth);
            852: }
            853:
            854: } // namespace details

    Aborted

例外を投げる部分でスタックトレースを含める必要があるため、
既存のライブラリなどが投げる例外には使用できないが、
自分でライブラリを作る際には役に立つのではないか。
