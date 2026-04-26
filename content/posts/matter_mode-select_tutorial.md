---
# description: ""
showTableOfContents: true
tags: ["IoT", "C++", "ESP32", "esp-matter", "Matter", "Mode Select"]
title: "esp-matter でモードセレクトを実装する"
type: "post"
date: 2026-04-26
---

## はじめに

Matter には Mode Select という、単一選択式の設定項目を追加することができる。

`esp-matter` を用いて Mode Select を実装することができるが、\
ドキュメントが簡素で分かりづらいので保管しながら備忘録として残しておく。

{{< alert "error" >}}
Mode Select クラスタは、各エンドポイントにつき1つまでしか設定できない。 \
複数の Mode Select を実装したい場合は、それぞれに対してエンドポイントを実装する。
{{< /alert >}}

## 実装

Light サンプルにMode Select用のエンドポイントを追加していく。

### 概要

今回は、工場出荷時のデータ(ファクトリーデータ)に選択肢情報を書き込み、\
esp-matter 側で読み取る方式を用いる。

そのため、まずはファクトリーデータを生成&書き込みを行う。

### パーティションの生成

パーティションを生成するためには、 `mfg-tool` というものを使う。
今回は `esp-matter` を使用しているので、専用の `esp-matter-mfg-tool` というものが利用できる。

esp-matter-mfg-tool が存在しない場合、以下のコマンドでインストールすることができる。

```bash
python3 -m pip install esp-matter-mfg-tool
```

次に、esp-matter-mfg-toolを用いてパーティションを作成する。

```bash
esp-matter-mfg-tool -cn "My Product" -v 0xFFF2 -p 0x8001 --pai \
-k ~/esp-matter/connectedhomeip/connectedhomeip/credentials/test/attestation/Chip-Test-PAI-FFF2-8001-Key.pem \
-c ~/esp-matter/connectedhomeip/connectedhomeip/credentials/test/attestation/Chip-Test-PAI-FFF2-8001-Cert.pem \
-cd ~/esp-matter/connectedhomeip/connectedhomeip/credentials/test/certification-declaration/Chip-Test-CD-FFF2-8001.der \
--supported-modes "0/label1/2" "1/label2/2"`
```

各オプションの意味は以下のとおりである。
|オプション|意味|詳細|
|:-:|:-:|:-:|
|-cn "My Product"|Common Name|デバイスの表示名|
|-v 0xFFF2|Vender ID (VID[^VPID])|製造元ID (0xFFF1~0xFFF4)はテスト用|
|-p 0x8001|Product ID (PID[^VPID])|製品ID (0x8000~0x801F)はテスト用|
|--pai|Product Attestation Intermediateの使用|PAI証明書と鍵を使用し、製品の正当性を証明する設定の有効化|
|-k|PAI秘密鍵|用意されている秘密鍵へのパス|
|-c|PAI証明書|用意されている証明書へのパス|
|-cd|Certification Declaration|デバイスがCSA認証を受けていることを示す宣言書|
|--supported-modes|Mode Select選択肢|Mode Select の選択肢を記述|

[^VPID]:
    VID は製造元を保証するIDで、製品リリース前にCSAに申請する必要がある。
    PID は製品IDで、0x8000~8x801F はテスト用なので、サンプルとして使用できる[デバイス認証証明書(DAC)](https://github.com/project-chip/connectedhomeip/blob/080bb5730aeed4019fdde46401208d74a546f5bb/src/credentials/examples/ExampleDACs.h)が利用できる。
    今回は `~/esp-matter/connectedhomeip/connectedhomeip/credentials/test/attestation/` 内の秘密鍵と証明書を使用した。
    ([参考リンク](https://developers.home.google.com/codelabs/matter-device-virtual?authuser=0&hl=ja#create-a-developer-project))

`--supported-modes` では、モードID、ラベル、エンドポイントを指定して入力する。 \
フォーマットは `<mode-id>/<label>/<endpoint-id>` である。

`mode-id` 選択肢に対応する数値を指定する。
`label` は任意の文字列で、これが選択肢のラベルとなる。
Mode Select クラスタは、各エンドポイントにつき最大1つまでなので、<endpoint-id> を指定する。
(今回は、Lightサンプルに新たなエンドポイントを実装するため、 `2` と設定している。)

上記のような設定でコマンドを実行すると、`./fff2_8001/<uuid>/<uuid>.bin` が生成される。
<uuid> はコマンドを実行するたびに変化し、 `.bin` ファイルが生成されたデータである。

### ファクトリーデータの書き込み

次に、ファクトリーデータ (`.bin`ファイル) を書き込む。

`./partitions.csv` を見ると、以下のように記載されている。

```csv
# Name,   Type, SubType, Offset,  Size, Flags
# Note: Firmware partition offset needs to be 64K aligned, initial 36K (9 sectors) are reserved for bootloader and partition table
esp_secure_cert,  0x3F, ,0xd000,    0x2000, encrypted
nvs,      data, nvs,     0x10000,   0xC000,
nvs_keys, data, nvs_keys,,          0x1000, encrypted
otadata,  data, ota,     ,          0x2000
phy_init, data, phy,     ,          0x1000,
ota_0,    app,  ota_0,   0x20000,   0x1E0000,
ota_1,    app,  ota_1,   0x200000,  0x1E0000,
fctry,    data, nvs,     0x3E0000,  0x6000
```

ファクトリーデータは `fctry` に書き込むので、開始位置 `0x3E0000` を控えておく。

書き込みには `esptool.py` を使用する。
オプションにはデバイスへのパスと書き込み開始位置、ファクトリーデータのパスを指定する。

```bash
esptool.py \
	-p /dev/ttyACM0 \
	write_flash 0x3E0000 \
	./out/fff2_8001/ebb621a9-bc8b-4136-8688-fb31b4722606/ebb621a9-bc8b-4136-8688-fb31b4722606-partition.bin
```

これにより、デバイスの `fctry` パーティションに選択肢を含めたファクトリーデータを書き込むことができた。

### menuconfig の設定

Mode Select を使うために、 `menuconfig` から設定を行う。

まずは、選択肢情報が `fctry` に格納されているので、それを利用する設定を行う。
`/chip-factory_namespace` で検索を行い、パーティションラベルに `fctry` を設定する。
(設定項目ID: `CHIP_FACTORY_NAMESPACE_PARTITION_LABEL`)

![fctryを読み込む設定](/Portfolio/images/posts/matter_mode-select_tutorial/chip-factory_namespace.png)

次に、MODE_SELECT を使うための設定を行う。
`/mode select` で検索し、2つの設定を行う。

1. Mode Select 自体の有効化: `SUPPORT_MODE_SELECT_CLUSTER` を `yes` に設定する。
2. Mode Select を使うエンドポイントの数: `ESP_MATTER_MODE_SELECT_CLUSTER_ENDPOINT_COUNT` を設定する。(今回は1つにしたいので、 `1` に設定した)

![Mode Select 有効化](/Portfolio/images/posts/matter_mode-select_tutorial/menuconfig_mode-select.png)

これにより、Mode Select を使う下準備が完了した。

### プログラムの実装

ここからは、実際にエンドポイントクラスタ(もといエンドポイント)を実装する。

まずは、エンドポイントを生成し、Matterに登録する。
この前に `endpoint::extended_color_light::create(...)` でエンドポイントを生成しているため、
以下のMode SelectエンドポイントのエンドポイントIDは `2` である。\
(念のため、IDをログ出力している。)

```cpp
// Set mode options for ModeSelect endpoint
endpoint::mode_select::config_t ms_config;
endpoint_t* ms_endpoint =
    mode_select::create(node, &ms_config, CLUSTER_FLAG_SERVER, nullptr);
ABORT_APP_ON_FAILURE(
    ms_endpoint != nullptr,
    ESP_LOGE(TAG, "Failed to create mode select endpoint"));
ms_endpoint_id = endpoint::get_id(ms_endpoint);
ESP_LOGI(TAG, "Mode select created with endpoint_id %d", ms_endpoint_id);
```

次に、選択肢の登録を行う。
`StaticSupportedModesManager` は、
`--supported-modes` で生成したファクトリーデータから自動で選択肢を読み取る。

それを `setSupportedModesManager(...)` で登録することで、選択肢を反映させることができる。

```cpp
static ModeSelect::StaticSupportedModesManager sStaticSupportedModesManager;
sStaticSupportedModesManager.InitEndpointArray(get_count(node));
ModeSelect::setSupportedModesManager(&sStaticSupportedModesManager);
```

## 動作確認

以上を実装したMatterデバイスをHome Assistantに登録すると、
`設定→デバイスとサービス→エンティティ` からモードを変更することができるようになっている。

![Mode Selectの動作確認](/Portfolio/images/posts/matter_mode-select_tutorial/ha_mode-select.png)
