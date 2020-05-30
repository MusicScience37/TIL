CSRF
===========

Cross-Site Request Forgeries (CSRF, XSRF)
は Cookie にセッション情報があることを利用して
他のサイトから javascript などでリクエストを送信する攻撃。

Cookie に
HTTP Only とか Secure の設定をかけていても、
HTTP リクエストを送信する際に
Cookie を含めるという基本的な部分は変わらないため、
他のサイトに javascript を仕込んでおくことで
セッション情報を含んだ Cookie 付きの
HTTP リクエストを送信することができる。

この攻撃を防ぐには、
リクエストが自分のサイト内から正規の手順で出力されたか
チェックする必要がある。

CSRF トークンは対策の 1 つで、
あらかじめ GET リクエストで取得可能なトークンを
POST リクエストに含める。
具体的には、

- サーバサイドレンダリングでページに hidden 属性の
  トークンを含めておくことで
  form の送信時に一緒にトークンを送信させる。
- API に GET リクエストを送ればトークンが取得できるようにしておき、
  POST リクエストに載せるようにする。

などの方法がある。
サーバ側のチェックの仕方としては、

- トークンを javascript から見えない HTTP Only の Cookie にも含めるようにし、
  Cookie のトークンとリクエストボディのトークンが一致することを確認する。

などがある。

GET リクエストでトークンが取得できるとなると、
一見 javascript から GET リクエストをすれば良いように見えるが、
他のサイトからリクエストが送信される場合は、
Same Origin Policy が守ってくれる。
Same Origin Policy は、
レスポンスが他のサイトの javascript から読めないようにするもので、
デフォルトで有効になっている。
あとは、
自分のサイト自身に javascript を仕込まれる
Cross-Site Scripting (XSS) 脆弱性の対策なども行うことで、
CSRF を防いでいく。
