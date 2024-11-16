---
# description: ""
showTableOfContents: true
tags: ["Android", "Android Studio", "Jetpack Compose", "Firebase", "FastAPI", "Kotlin", "Python", "Firestore"]
title: "支払い重みに対応した割り勘アプリ「Split」"
type: "post"
date: 2024-10-16
---

![アプリアイコン](/Portfolio/images/posts/split_app/icon.svg)

## 概要
- 「先輩は5%多く払う」
- 「飲まない人は半額」

ような状況に対応するための割り勘アプリ。

## 主な機能
- ルームごとに支払い情報を管理
- 支払い重みで割り勘計算
- 1円/10円/100円単位などでの割り勘

## 技術
アプリの全体のイメージは以下のようになっている。
![全体のイメージ図](/Portfolio/images/posts/split_app/split_structure.svg)

データの管理は[Firestore](https://firebase.google.com/docs/firestore?hl=ja)で行う
**三層アーキテクチャ**のような構成になっている。
データの書き込みはAPIから行うことで、アプリから直接DBに書き込むことを禁止している。

FirestoreとAndroidアプリはFirebaseのSDKを利用して、
Firestoreが更新されたときにAndroidアプリ画面上に即座に反映される仕組みになっている。

## プログラム
### Android
{{< linkcard "https://github.com/mutoxu-N/SplitApp/commits/master/" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/SplitApp)

### API
{{< linkcard "https://github.com/mutoxu-N/SplitAPI" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/SplitAPI)