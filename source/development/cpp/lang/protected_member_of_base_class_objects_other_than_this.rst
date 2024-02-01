this ポインタ以外の基底クラスオブジェクトの protected メンバについて
=======================================================================

C++ のクラスにおける protected メンバは派生クラスからアクセスできると思っていたが、
少し追加の条件があった。

`C++ リファレンスのアクセス指定子の説明 <https://ja.cppreference.com/w/cpp/language/access>`_
から引用すると、protected メンバへアクセスできるのは

    1) Base のメンバおよびフレンド。
    2) Base から派生したあらゆるクラスのメンバおよびフレンド (C++17未満)。
       ただし Base から派生した型のオブジェクト (this を含みます) に対する操作のときだけです。

となっている。
ここで、派生クラス自身のオブジェクトの protected メンバでなければ使えない
という制限があることに注意。

例えば、次のようなソースコードはコンパイルできない。

.. code-block:: cpp

    class Base {
    protected:
        void func();
    };

    class Derived : public Base {
        void process(const Base& obj) {
            obj.func();  // ←ココでアクセスできない。
        }
    };

上記のようなことがしたい場合は、次のようにする。

.. code-block:: cpp

    class Base {
    protected:
        void func();
        static void call_func(const Base& obj) {
            obj.func();
        }
    };

    class Derived : public Base {
        void process(const Base& obj) {
            call_func(obj);
        }
    };

基底クラス自身は自分の protected メンバへアクセスできる上に、
基底クラスの protected な static 関数は派生クラスからアクセスできるため、
上記のソースコードはコンパイルできる。
上記なら friend 指定のように private なメンバへのアクセスとかまで許可しなくて良い。
