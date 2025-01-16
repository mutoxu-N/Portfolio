---
# description: ""
showTableOfContents: true
tags: ["Android","Android Studio","Firebase","Firestore","Jetpack Compose"]
title: "ブックマークを管理するアプリ「MyBookmark」"
type: "post"
date: 2024-05-06
---

## 要約
Firebase SDKを使ってみたかったので作ったアプリ。
[Firebase Authentication](https://firebase.google.com/products/auth?hl=ja)で、
Googleアカウントでログインすることができ、
アカウントごとにブックマークの情報を[Firestore](https://firebase.google.com/products/firestore?hl=ja)に保存できる。
![アプリ画面](/Portfolio/images/posts/my_bookmark/screen.webp)

## 主要機能
- URLとタイトルの保存
- タグの追加
- タグで検索
- 共有機能からブックマークを追加


## プログラム
{{< linkcard "https://github.com/mutoxu-N/MyBookmarkApp" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/MyBookmarkApp)