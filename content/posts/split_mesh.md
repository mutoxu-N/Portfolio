---
# description: ""
showTableOfContents: true
tags: ["C++", "大学", "幾何"]
title: "三角形メッシュを連続する2領域に分割する"
type: "post"
date: 2024-07-11
---

## 要約

OBJ ファイルから読み込んだ三角形メッシュを\
連続する 2 領域に分割するプログラムを作成した。

![実行結果例](/Portfolio/images/posts/split_mesh/squirrel_med.png)

## プログラム

{{< linkcard "https://github.com/mutoxu-N/Study/tree/main/split_mesh" >}}
[GitHub](https://github.com/mutoxu-N/Study/tree/main/split_mesh)

## アルゴリズム

プログラム全体のアルゴリズムを簡単に説明する。

### 1. ハーフエッジデータ構造の構築

三角形メッシュを効率的に保持・探索するためのデータ構造として、\
**ハーフエッジデータ構造**がある。\
(※三角形メッシュ以外にも使用できるが、三角形メッシュだと良い特徴がある。)

頂点数を $n$、面数を $f$ とすると、
ハーフエッジデータ構造では $3f + n$ のメモリ空間でメッシュを表現できる。

### 2.グラフラプラシアンの構築

ラプラシアン行列 $\boldsymbol{L} = (l_{ij})$ を構築する。\
$d_i$ は頂点 $i$ の次数。

$$
l_{ij} =
\begin{cases}
    d_i & \text{if } i=j, \newline
    -1 & \text{if } ij\in E, \newline
    0 & \text{otherwise.}
\end{cases}
$$

ここで、 $l_{ij}$ はほとんど$0$の**疎行列**となるため、\
Eigen の SparseMatrix を用いてメモリを節約する。

### 3. Fiedler ベクトル

ラプラシアン行列は半正定値行列であるので、\
すべての固有値は非負である。

また、$\boldsymbol{L}\cdot \boldsymbol{1} = \boldsymbol{0}$ が成り立つため、\
ラプラシアン行列の最小固有値は $0$ である。

ここで、2 番目に小さい固有値を**Fiedler 値**と呼び、\
その固有ベクトルを**Fiedler ベクトル**と呼ぶ。\
(Spectra を用いて計算する。)

### 4. メッシュ分割

メッシュを 2 領域に分割する問題は**NP 困難**なので連続緩和した問題を考えると、\
最適解が Fiedler ベクトルになる事が知られている。

ここで、Fiedler ベクトルの各要素の値を閾値で分類すると\
二つの領域に分割することができる。

Fiedler ベクトルの各要素の値を正負で分割すると、\
連結する 2 領域に分割できる。\
この分割を `sign cut` と呼ぶ。

Fiedler ベクトルの各要素の中央値を閾値として\
グラフを分割する `median cut` を考えることもある。

## 実行結果例

GitHub には出力 OBJ ファイルもあるので、\
MeshLab などで開いて確認してみてほしい。

### Armadillo (sign cut)

![Armadilloに対するsign cutの例](/Portfolio/images/posts/split_mesh/armadillo5000_sign.png)

### Armadillo (median cut)

![Armadilloに対するmedian cutの例](/Portfolio/images/posts/split_mesh/armadillo5000_med.png)
