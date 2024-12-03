---
# description: ""
showTableOfContents: true
tags: ["Python","Flet","大学"]
title: "KATAMINOを解いて分かりやすく表示するアプリ"
type: "post"
date: 2024-12-02
---


## 概要
大学の講義でパズルゲーム「[カタミノ](https://en.gigamic.com/puzzles/104-katamino.html)」の詰め込みについて扱った。
それを参考に、
使用するミノと盤面の大きさを指定して、 
詰め込み計算を行うアプリを作成した。


## 画面例
オーソドックスな12x5のカタミノ。
![画面例1](/Portfolio/images/posts/katamino/gui1.png)


Fミノを使用しない11x5の詰め込み。
![画面例2](/Portfolio/images/posts/katamino/gui2.png)

詰め込み不可能ならこのように表示される。
![画面例3](/Portfolio/images/posts/katamino/gui3.png)

## プログラム
Fletを始めて触ったのでメンテナンス性の低いコードになってしまっている。
良い書き方を勉強したい。

{{< linkcard "https://github.com/mutoxu-N/KataminoSolver" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/KataminoSolver)