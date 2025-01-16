---
# description: ""
showTableOfContents: true
tags: ["高校","Defold","Lua"]
title: "素因数分解アプリ"
type: "post"
date: 2019-09-16
---

## 要約
$2, 3, 5, 7, 11, 13, 17, 19$ の合成数が与えられるので、
その数字を正しい素因数で割り続けるアプリ。
高校の文化採用に作成した。

部室にAndroidタブレットがあったため、
いろいろなアスペクト比の画面でも正常に動くようなレイアウトを練習するために作成した。
画面の向きによってレイアウトが変化する。

![横画面](/Portfolio/images/posts/factoring/horizontal.png)

![縦画面](/Portfolio/images/posts/factoring/vertical.png)


Windows用ダウンロード: [GitHub](https://github.com/mutoxu-N/Factoring/releases/tag/windows)


## 閑話
僕は一度だけ53問目まで行きましたが、それ以上解いた人は未確認です。

当時、文化祭に来ていた小学生が**43問目**まで解いていました。
5問ごとに素因数が1つ増えるので、
$n$問目の素因数の数は $\lfloor \frac{n}{5} \rfloor + 2$ 個になります。

## プログラム
{{< linkcard "https://github.com/mutoxu-N/Factoring">}}
ソースコード: [GitHub](https://github.com/mutoxu-N/Factoring)