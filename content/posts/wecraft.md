---
# description: ""
showTableOfContents: true
tags: ["高校", "Defold", "Lua"]
title: "WECraft"
type: "post"
date: 2019-09-13
---

![タイトル画面](/Portfolio/images/posts/wecraft/title.png)

## 要約
高校時代に文化祭用に、[Defold](https://defold.com/)で作成したゲーム。
ゲームシステムは[OHOL](https://store.steampowered.com/app/595690/One_Hour_One_Life/?l=japanese)のような形で、
目標のアイテムを作成したらクリア。

{{< linkcard "https://github.com/mutoxu-N/WECraft/releases/tag/v1.0" >}}
ダウンロード: [GitHub](https://github.com/mutoxu-N/WECraft/releases/tag/v1.0)

## 隠し要素
### 最高難易度
WECraftの難易度には、難易度順に4つを選択することができる。
- EASY
- NORMAL
- HARD
- EXTREME

![難易度一覧](/Portfolio/images/posts/wecraft/difficulty.png)

実は、最も難しい難易度として **IMPOSSIBLE** が用意されている。

{{< collapse "0" >}}
難易度選択画面ウィンドウで右上の端をクリックすると、
難易度IMPOSSIBLEをプレイすることができる。
現在、IMPOSSIBLEのクリア者は、
僕と友人の2人だけしか確認していない。
{{< /collapse >}}


### チートモード
ある操作を行うとチートモードを起動することができ、
- アイテムの取得
- テレポート
- 移動速度/腹減り速度/満腹度最大値 の変更

が行える。

{{< collapse "0" >}}
チートモードに移動するには、パスワードが必要である。
パスワードの入力手順は次の通り。

1. プレイヤーの向きが反転するまで、`K` を長押しする。
2. その状態で `marron` と入力する。

正常に動作すると管理者画面が表示される。
![難易度一覧](/Portfolio/images/posts/wecraft/admin.png)

#### アイテムID
アイテムの取得にはアイテムIDが必要である。
アイテムIDの確認は [`recipes.lua`](https://github.com/mutoxu-N/WECraft/blob/master/main/assets/items/recipes.lua)の
`items` から確認できる。

{{< /collapse >}}


## プログラム
{{< linkcard "https://github.com/mutoxu-N/WECraft" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/WECraft)