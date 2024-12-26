---
# description: ""
showTableOfContents: true
tags: ["Android", "Android Studio", "Jetpack Compose", "Kotlin"]
title: "広告の無い数独アプリを作りました"
type: "post"
date: 2024-12-26
---

## 概要
祖母が数独をやりたがっていたが、既存のアプリは広告が多いと文句を言っていたため、広告の無いアプリを作成した。
![画面例](/Portfolio/images/posts/sudoku_app/screen.png)

## データ
数独の問題データは、[3 million Sudoku puzzles with ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings) から取得した。
`rating` を基に以下の難易度に分類し、各10000問をランダムに選択して、問題をアプリに埋め込んだ。

|難易度|レーティング|
|:-:|:-:|
|EASY|0.0|
|NORMAL|0.1 ~ 2.0|
|HARD|2.1 ~|

## 機能
- 難易度選択機能
- クリア判定
- メモ機能
- アプリ再開時に進捗状況を読み込む
- 2ヶ国語対応 (日本語、英語)

## プログラム
{{< linkcard "https://github.com/mutoxu-N/SudokuApp" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/SudokuApp)