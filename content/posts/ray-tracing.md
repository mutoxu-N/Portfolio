---
# description: ""
showTableOfContents: true
tags: ["C++","大学","幾何"]
title: "レイトレーシングを使用してOBJをレンダリング"
type: "post"
date: 2024-06-06
---

## 要約
OBJファイルから読み込んだ三角形メッシュを、 \
レイトレーシングを利用してレンダリングするプログラムを作成した。

ナイーブな実装なので非常に低速。\
[kd-tree](https://ja.wikipedia.org/wiki/Kd%E6%9C%A8)のようなデータ構造を使用すると高速になりそう。

![実行結果例](/Portfolio/images/posts/ray-tracing/bunny.png)

## プログラム
{{< linkcard "https://github.com/mutoxu-N/Study/tree/main/ray-tracing" >}}
[GitHub](https://github.com/mutoxu-N/Study/tree/main/ray-tracing)

## アルゴリズム
プログラム全体のアルゴリズムを簡単に説明する。

### 1. メッシュの正規化
メッシュの頂点群の境界球を求める。 \
ここでは、[Ritterのアルゴリズム](https://en.wikipedia.org/wiki/Bounding_sphere#Ritter's_bounding_sphere)を用いる。

求めた境界球の中心と半径を用いて、\
メッシュが単位球の内部に入るように正規化する。

### 2. レイトレーシング計算
出力画像の各画素の中心から ray を飛ばし、メッシュの色を計算する。

メッシュの全面と ray の交差判定を行い、 \
交差している面の中で視点に最も近い面を選択する。\
(ここで `kd-tree` を用いると、探索する面を減らせる。)

その面の法線ベクトルを用いて、面の色を算出し、\
出力画像の画素に反映する。

### 3. ray と三角形の交点
ここでは、交点を直接求めるわけではない。 \
三角形の各頂点ベクトル $\boldsymbol{a}, \boldsymbol{b}, \boldsymbol{c}$ と ray の支点ベクトル $\boldsymbol{p}$、方向ベクトル $\boldsymbol{d}$ から\
交点の重心座標 $\boldsymbol{u}$ を計算する。

重心座標の定数倍 $k\cdot \boldsymbol{u}$ の各要素は、以下のような3x3行列の行列式を用いて計算できる。
$$ k\cdot u_1 = det(\boldsymbol{d}, \boldsymbol{b}-\boldsymbol{p}, \boldsymbol{c}-\boldsymbol{p}) $$
$$ k\cdot u_2 = det(\boldsymbol{d}, \boldsymbol{c}-\boldsymbol{p}, \boldsymbol{a}-\boldsymbol{p}) $$
$$ k\cdot u_3 = det(\boldsymbol{d}, \boldsymbol{a}-\boldsymbol{p}, \boldsymbol{b}-\boldsymbol{p}) $$

重心座標 $\boldsymbol{u}$ は各要素の総和が$1$となるようなものであるため、 \
$k = k\cdot u_1 + k\cdot u_2 + k\cdot u_3 $ で計算できる。

従って、$k\cdot \boldsymbol{u}$ を $k$ で割ることで重心座標が求められる。