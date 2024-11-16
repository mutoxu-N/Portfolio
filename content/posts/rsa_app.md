---
# description: ""
showTableOfContents: true
tags: ["大学","Android","Android Studio","Kotlin", "Jetpack Compose"]
title: "RSA電卓"
type: "post"
date: 2024-07-21
---

## 概要
RSA暗号の暗号化・復号化を計算するための電卓アプリ。
2つの素数を入力し、上段で暗号化、下段で復号化の演算を行っている。

![アプリ画面](/Portfolio/images/posts/rsa_app/screen.webp)

## 解説
### 鍵の生成
2つの素数 $p, q$、暗号化したい数値(平文) $m \notin \lbrace p, q \rbrace$ において、
$n$、$\phi(n)$[^phi]を定義する。
[^phi]: [オイラーのφ関数 (Wikipedia)](https://ja.wikipedia.org/wiki/%E3%82%AA%E3%82%A4%E3%83%A9%E3%83%BC%E3%81%AE%CF%86%E9%96%A2%E6%95%B0)

$$ n = p \cdot q $$ 
$$ \phi(n) = (p-1)(q-1) $$

$n, m$ は互いに素なのでオイラーの定理[^euler]より以下が成り立つ。
$$ m^{\phi(n)} \equiv 1 \quad(\bmod n)$$
$$ m^{\phi(n)+1} \equiv m \quad(\bmod n)$$

[^euler]: [オイラーの定理 (Wikipedia)](https://ja.wikipedia.org/wiki/%E3%82%AA%E3%82%A4%E3%83%A9%E3%83%BC%E3%81%AE%E5%AE%9A%E7%90%86_(%E6%95%B0%E8%AB%96))

ここで、暗号化鍵(公開鍵) $d$、復号化鍵(秘密鍵) $e$ は以下のように表すことができ、
$d$ を決めると、拡張ユークリッドの互除法[^euclid]を用いて $e$ を求められる。($d,e > 0$)
[^euclid]: 拡張ユークリッドの互除法でMOD逆元を計算することができる。[参考](https://qiita.com/sesame0224/items/f2ac77c367f588c0d29d)

$$ d \cdot e \equiv 1 \quad (\bmod\ \phi(n)) $$ 

以上より、
- 公開鍵: $(d, n)$
- 秘密鍵: $(e, n)$

を求められた。

### 暗号化
平文 $m$ を、公開鍵を使って暗号化し、暗号文 $s$ を得る。
$$ s = m^d \mod n $$

### 復号化
暗号文 $s$ を、秘密鍵を使って複合化し、平文 $m$ を得る。
$$ m = s^e \mod n $$

### 復号できているか確認
$d \cdot e \equiv 1 \quad (\bmod\ \phi(n))$ より、
$d \cdot e = k\phi(n) + 1\quad (k\in \N)$と置く。

$$ s^e \equiv m^{d\cdot e} \equiv m^{k\phi(n)+1} \equiv m^{\phi(n)} \cdot m^{\phi(n)} \cdots m^{\phi(n)}\cdot m \equiv m\quad (\bmod n)$$

$m = s^e\mod n$ となり、復号できていることがわかる。

### 高速指数演算
$a^e\mod n$ の計算を高速に行う必要がある。

まず、$e$ を $m$ ビット整数と仮定し各桁を $b_i \in \lbrace 0, 1 \rbrace$ で表す。
$$ e = \sum_{i=0}^{m-1} b_i\cdot 2^i $$ 
$$ a^e = \prod_{i=0}^{m-1} a^{b_i 2^i} = \prod_{i=0}^{m-1} (a^{2^i})^{b_i}$$ 

ここで次の式が成り立つので、下位ビットから計算すると $ O(m) = O(\log n) $で計算することができる。
また、計算途中でも $\bmod n$ を取れるので、オーバーフローを防ぎながら計算できる。
$$ a^{2^{i+1}} = (a^{2^i})^2 \bmod n $$


## プログラム
{{< linkcard "https://github.com/mutoxu-N/FastExponentiationApp" >}}
ソースコード: [GitHub](https://github.com/mutoxu-N/FastExponentiationApp/blob/master/app/src/main/java/com/github/mutoxu_n/fastexponentiation/MainActivity.kt)