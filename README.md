# rollbook

卒業論文を書く意志のない学生たちをきちんと留年させるための欠席簿。
学校来ないんだから。宿題もやって来んし。理由にならない毎度の言い訳は聞き飽きた。
卒業研究の時間は空き時間じゃない。ましてやバイトの時間でもない。
何度言ったか。
学力が卒業のレベルになかったら、来年以降、学力つけて再挑戦したらいい。
あるいはこの際、早めに学業をあきらるか。

このアプリで月曜 1 時間目から金曜 5 時間目まで学生自身に出席を記録させる。
バージョン 0.4 からは時間外の申告も記録する。
記録と同時に「自分はこの時間、何をしているか」をレポートさせる。
レポートが短い時、出席を記録しない。

記録にない過去の欠席状況見ますか？ 俺の言ってること、納得するよ。
体たらくは
[redmine](https://redmine.melt.kyutech.ac.jp)
でも想像つくはず。

## TODO

* ボケは出席ボタンだけ押して外出する。部屋にいても寝ている。電気の無駄です。
  わからんやつは何してもわからん。ムダ。

* redmine のチケットへのリンクを設けるか。

* 彼、彼女の申告する「授業のある時間」を表示する。

* やっぱ、出席/欠席だけじゃなく、遅刻・早退も必要だ。

* BUG 0.4.1 --- 休み時間になった時にウェークアップしてしまう。

* 日付をクリックして現れる今日の attends、タイムスタンプを表示する。

* 評価をするユーザ、つまり俺の認証。

* raco exe --gui で作成した app が動作しない。

  スレッドの扱いが十分ではない。GUI のパーツが出来上がる前にメインスレッドが終わっちゃうのかな。
  (thread-wait thd) すると GUI パーツに CPU が回らない。

* raco exe （--gui なし）でビルドしたバイナリであっても、
  サーバからダウンロードしたままでは
  Apple のプロテクトがあってダブルクリックでは動かない（チケット #3743）。

* 本日の将来コマにとりあえず欠席が入ってしまう。

  欠席を積極的に報告するメカニズムが必要。

## DONE

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
