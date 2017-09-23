# rollbook

卒業論文を書く意志のない学生たちを留年させるための欠席簿。
月曜 1 時間目から金曜 5 時間目まで、その時間に何をしているのか、
学生自身に redmine の [チケット](http://redmine.melt.kyutech.ac.jp)
で申告させ、その記録と進行状況を出席とする。

卒論書くための学力・知識の不足は自分でもわかってると言うくせに、
学校来ないし、宿題もやってこん。
一週間の大半を占める「卒業研究の時間」は空き時間やバイトの時間では決してない。
お勉強の時間だぞ。何度言ってもわからない。

そんな人たちは学力つけてから、来年以降、卒論再挑戦しなさい。
あるいはこの際、早めに学業をあきらめるか。

## TODO

* なんで欠席簿が必要になるか、理解できない学生たちだ。
  出席ボタンだけ押して外出する。
  授業時間終了間際に出現し出席ボタンだけ押す。
  部屋にいても寝ている。
  そういうのは欠席扱いにする。

* 彼、彼女の申告する「授業のある時間」を表示する。

* 評価をするユーザ、つまり俺の認証。

* raco exe --gui で作成した app が動作しない。

  スレッドの扱いが十分ではない。
  GUI のパーツが出来上がる前にメインスレッドが終わっちゃうのかな。
  (thread-wait thd) すると GUI パーツに CPU が回らない。

* raco exe （--gui なし）でビルドしたバイナリであっても、
  サーバからダウンロードしたままでは
  Apple のプロテクトがあってダブルクリックでは動かない（チケット #3743）。

* 本日の将来コマにとりあえず欠席が入ってしまう。

  欠席を積極的に報告するメカニズムが必要。

## DONE

* 土日フィルター。フィルタじゃなく、テーブルに色つけることで対処する。

* Racket 6.8 のバイナリ --- imac3 で作れるようになった。raco-6.8。

* redmine のチケットへのリンクを設けた。message で #nnnn を入れる。

* 日付をクリックして現れる今日の attends、タイムスタンプを表示する。
  JST に直して。

* 時間ごとコメントの表示。
  日付をクリックしたら下の時間外 attends 含めて表示する。

* 時間外 attends.

* バージョン表示

* まったく attend を実行しない学生は欠席もつかない。

  &rArr; ユーザ全員のその日の 0 時間目に欠席を入れるボタンを attends 上に作る。

* スリープして自分で起きる。

  &rArr; アイコン化でごまかす。もっといい方法あるような。

* メッセージの長さが 10 文字未満だと「もっと具体的に！」とクレームする。

* そろそろ本番環境へ。本番は vm2017 の mysql を使う。
  mysql の新しいユーザを作り、
  クライアント（学生）にはバイナリにコンパイルしたコードを渡す。
  mysql のユーザアカウント隠蔽のためだ。

---
hkimura
