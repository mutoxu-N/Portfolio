---
# description: ""
showTableOfContents: true
tags: ["IoT", "C++", "ESP32", "esp-matter", "Matter"]
title: "ESP32を使ったMatterデバイス開発の環境構築"
type: "post"
date: 2026-04-18
---

## はじめに

Espressif社のマイコン **ESP32** とESP用のMatterライブラリ **esp-matter** を使ってMatterデバイスを開発する際の環境構築の備忘録。

今回の開発で使うものは以下のとおりである。

### ESP32

今回は [`ESP32-C6-DevKitC-1`](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/index.html) という開発ボードを用意する。
ESP32-C6 は Wi-Fi、Bluetooth LE、Zigbee、Thread に対応したチップであり、これらの規格を扱えるMatterデバイスの開発に適している。

### VSCode

言わずと知れたテキストエディタ (もはやIDE)
{{< linkcard "https://code.visualstudio.com/" >}}

これに ESP-IDF という拡張機能を導入する。
{{< linkcard "https://marketplace.visualstudio.com/items?itemName=espressif.esp-idf-extension" >}}

### WSL

Windows上でLinuxを実行するためのもの。\
今回は `Ubuntu 24.04.3 LTS` を使い、VSCodeでWSL内のファイルを編集して開発を行う。

{{< alert "warning" >}}
ESP-IDF自体はWindowsでの開発も可能だが、esp-matterはLinuxでの開発が基本となっているので、WindowsユーザーはWSLを利用しよう。
{{< /alert>}}

### ESP-IDF

ESP32の開発を行うためのライブラリ
{{< linkcard "https://github.com/espressif/esp-idf" >}}

### esp-matter

ESP-IDF と併せて、ESP32上でMatterデバイスを開発するためのライブラリ
{{< linkcard "https://github.com/espressif/esp-matter" >}}

## 環境構築

長くなるので、WSL、VSCode、ESP-IDF(拡張機能)の導入方法は省略する。 \
以降は、ESP-IDF(拡張機能)がインストールされたVSCodeで、 \
WSL内のホームディレクトリを開いている前提で進めていく。

### ESP-IDF(ライブラリ)のインストール

#### バージョンの確認

[esp-matter](https://github.com/espressif/esp-matter)を見ると、
`ESP-IDF v5.5.1` の利用が推奨されている。 \
今回は、v5.5.1 をインストールするが、この部分は更新される可能性があるので、\
随時確認してほしい。

![ESP-IDFのバージョン](/Portfolio/images/posts/esp-idf_tutorial/esp-idf_version.png)

ここからは、公式ドキュメントが用意されているので、それを参考にする。
{{< alert "info">}}
ESP-IDF と esp-matter のドキュメントがあるので、基本は esp-matter の方を踏襲する。
{{< /alert >}}

{{< linkcard "https://docs.espressif.com/projects/esp-idf/en/v5.5.1/esp32c6/get-started/linux-macos-setup.html#" >}}
{{< linkcard "https://docs.espressif.com/projects/esp-matter/en/latest/esp32c6/developing.html#esp-idf-setup" >}}

#### 必要なパッケージのインストール

まずは、ESP-IDFで使用するパッケージをインストールする。

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

#### ESP-IDF のインストール

`~/esp/v5.5.1/esp-idf` 内にESP-IDFをダウンロードする。

```bash
mkdir -p ~/esp/v5.5.1
cd ~/esp/v5.5.1
git clone -b v5.5.1 --recursive https://github.com/espressif/esp-idf.git

```

以下を実行してインストール。

```bash
cd ~/esp/esp-idf
git submodule update --init --recursive;
./install.sh
```

#### ESP-Matter のインストール

`~/esp-matter` に esp-matter をインストールする。

まずは、 `esp-idf` を有効化する。

```bash
cd ~/esp/v5.5.1/esp-idf
source ./export.sh
```

次にesp-matterをダウンロード、インストールする。
{{< alert "info">}}
`./scripts/checkout_submodules.py --platform esp32 linux --shallow` と `./isntall.sh` の実行には時間がかかるので気長に待とう。
{{< /alert >}}

```bash
cd ~
git clone --depth 1 https://github.com/espressif/esp-matter.git
cd esp-matter
git submodule update --init --depth 1
cd ./connectedhomeip/connectedhomeip
./scripts/checkout_submodules.py --platform esp32 linux --shallow

cd ~/esp-matter
./install.sh
. ./export.sh
```

以上で、開発環境の構築は完了した。

## サンプルプロジェクトの実行

### 開発ボードをWSLに接続

購入した開発ボードをPCに接続しても、WSLからは認識されない。 \
WSL内でUSBが認識できるように設定を行う。

ここでは、 `usbipd` というツールを用いる。
{{< linkcard "https://github.com/dorssel/usbipd-win/releases" >}}

winget が使えるなら、以下のコマンドでインストールできる。

```powershell
winget install --interactive --exact dorssel.usbipd-win
```

次に、管理者権限で起動したコマンドプロンプト/PowerShell で

```powershell
usbipd list
```

を実行する。 \
USBデバイス一覧が出てくるので、開発ボードっぽいデバイスを選択する。 (今回は `1-1` )
![USBデバイス一覧](/Portfolio/images/posts/esp-idf_tutorial/usbipd_not-shared_example.png)

`STATE` が `Not Shared` になっているはずなので、これを `Shared` に変更する。 \
(ここに管理者権限が必要です。)

```powershell
usbipd bind --busid 1-1
```

次に、WSLにアタッチする。 \
開発をしているときは、常に以下のコマンドを実行し続ける必要がある。

```powershell
usbipd attach -awb 1-1
```

ここまで行うと、WSL内で

```bash
lsusb
```

を実行すると、ESP32-C6が認識されたことがわかる。

```
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 303a:1001 Espressif USB JTAG/serial debug unit
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

### 開発の前の設定

次に、開発時に必要な設定を行う。

まずは、ESP-IDFとesp-matterの有効化だ。\
これらのコマンドを実行することで、環境変数が設定され、各種ツールやライブラリが使えるようになる。

```bash
cd ~/esp/v5.5.1/esp-idf; source ./export.sh
cd =/esp-matter; source ./export.sh
```

これらはターミナルを起動するたびに設定する必要がある。

### サンプルプロジェクト

esp-matter のサンプルプロジェクトは、`~/esp-matter/examples/` に用意されている。\
まずは、単純な照明のサンプルを実行する。

```bash
cd ~/esp-matter/examples/light
```

#### 実行

実行する機器の種類を設定する。

```bash
idf.py set-target esp32c6
```

ここで設定される環境変数はターミナル再起動でリセットされてしまう場合があるため、 \
実行時にエラーが出たら以下を実行して環境変数を再設定する。

```bash
export ESP_MATTER_DEVICE_PATH=$ESP_MATTER_PATH/device_hal/device/esp32c6_devkit_c
```

次に、デバイスの接続ポートを設定する。\
VSCodeの下部バーにコンセントのようなマークが存在するのでクリックすると、デバイスのポートを選択できる。
![ポート選択画面](/Portfolio/images/posts/esp-idf_tutorial/esp-idf_port-list.png)

今回は1台しか接続していないので、ひとつだけ表示されているが、 \
複数台で開発する場合は適切に設定しよう。

ここまで設定すれば、あとは実行するだけである。 \
以下のコマンドで、ビルド&書き込みをした後、シリアル通信のモニターを自動表示することができる。

```bash
idf.py build flash monitor
```

「権限がない」と言われたら、デバイス権限を変更する。

```bash
sudo chmod 666 /dev/ttyACM0
```

モニターを閉じるときは `Ctrl+[` を押す。

#### 動作確認

デバイスが動作し始めると、スマホにデバイス追加画面が表示されるので、その指示に従ってデバイスを追加する。

{{< alert "error" >}}
著者の環境では、Wi-FiがWPA3だとWi-Fi接続に失敗するので、事前にスマホ側でWPA2のアクセスポイントに接続してから、デバイス追加を実行した。
{{< /alert >}}

接続のためのQRコードが必要な場合、以下のQRコードを利用する。 \
(PINを利用する場合: `34970112332`)

{{< linkcard "https://project-chip.github.io/connectedhomeip/qrcode.html?data=MT:Y.K9042C00KA0648G00" >}}

実際に HomeAssistant に追加すると以下のような操作パネルからデバイスを操作できる。
![HomeAssistantの操作パネル](/Portfolio/images/posts/esp-idf_tutorial/ha_sample.png)

## 豆知識

### menuconfig

`idf.py menuconfig` を実行するとプロジェクト設定を行うことができる。 \
(画面が表示されるまで時間がかかることがある。)

![menuconfigのトップ画面](/Portfolio/images/posts/esp-idf_tutorial/menuconfig.png)

この画面は Vim のような操作感で扱える。\
`/` で検索を行うことができるため、何か設定するときには検索するのが良い。

例えばログレベルを設定したい場合には`/LOG_LEVEL` で検索すれば良い。
![ログレベルの設定](/Portfolio/images/posts/esp-idf_tutorial/log_level.png)

### ターミナルの開始時の設定

VSCode を再起動するなど、開発時にターミナルを再起動したときには、 \
以下のコマンドで環境変数を再設定すると良い。

```bash
cd ~/esp/v5.5.1/esp-idf; source ./export.sh; cd ../../..
cd ~/esp-matter; source ./export.sh; cd ..
export ESP_MATTER_DEVICE_PATH=$ESP_MATTER_PATH/device_hal/device/esp32c6_devkit_c
```
