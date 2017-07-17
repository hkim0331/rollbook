# rollbook

卒業論文を書く意志のない学生たちをきちんと留年させるための出席簿。
だって学校来ないんだから。

月曜1時間目から金曜5時間目まで学生自身に出席を記録させる。

記録と同時に「自分はこの時間、何をしているか」をレポートさせる。
レポートが短い時、出席を記録しない。

## TODO

* 評価をするユーザの認証。つまりは俺なんだが。

* raco exe --gui で作成した app は動作しない。
  スレッドの扱いが十分ではない。GUI のパーツが出来上がる前にメインスレッドが終わっちゃうのかな。
  (thread-wait thd) すると GUI パーツに CPU が回らない。

* 本日の将来コマにとりあえず欠席が入ってしまう。

  &rArr; 欠席を積極的に報告するメカニズムが必要。

## DONE

* 時間ごとコメントの表示。忘れてた。
  日付をクリックしたら下の時間外 attends 含めて表示するか。

* 時間外の attends.

* バージョン表示

* まったく attend を実行しない学生は欠席もつかない。

  &rArr; ユーザ全員のその日の0 時間目に欠席を入れるようにする。


* スリープして自分で起きる。

  &rArr; アイコン化で済ます。もっといい方法あるような。

* メッセージが短いと、「もっと具体的に！」とかクレームする。

  &rArr; 10文字にした。

* そろそろ本番環境へ。本番は vm2017 の mysql を使う。
  mysql の新しいユーザを作り、
  クライアント（学生）にはバイナリにコンパイルしたコードを渡す。
  mysql のユーザアカウント隠蔽のためだ。


---
hkimura
