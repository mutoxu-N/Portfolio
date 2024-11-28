---
# description: ""
showTableOfContents: true
tags: ["Python","Kotlin","Android","Web","Flask","TensorFlow"]
title: "深層学習を用いたリバーシAI"
type: "post"
date: 2024-02-01
---

## 概要
大学の[iDSプログラム](https://www.chuo-u.ac.jp/gp/collaborate/program/information/)で、
Alpha Zeroのアルゴリズムを参考にしたリバーシアプリを作成した。
チームで作成したプロダクトで僕が担当したのは次の要素。
- 機械学習モデルの実装・学習
- APIの作成
- Androidアプリの作成


## 構成
簡単な構成は以下の通り。
![リバーシアプリの全体図](/Portfolio/images/posts/reversi_app/reversi.png)

クライアント側から現在の盤面とCPUの手を送信すると、 
サーバー側でCPUの手を計算して配置場所を返す仕組み。
Webアプリとしてブラウザ上でプレイすることができ、
同じAPIを使用したAndroidアプリからも
同様にプレイすることができる。

## 参考文献
[AlphaZero 深層学習・強化学習・探索 人工知能プログラミング実践入門](https://www.amazon.co.jp/AlphaZero-%E6%B7%B1%E5%B1%A4%E5%AD%A6%E7%BF%92%E3%83%BB%E5%BC%B7%E5%8C%96%E5%AD%A6%E7%BF%92%E3%83%BB%E6%8E%A2%E7%B4%A2-%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E5%AE%9F%E8%B7%B5%E5%85%A5%E9%96%80-%E5%B8%83%E7%95%99%E5%B7%9D-%E8%8B%B1%E4%B8%80/dp/4862464505)


