# yoiotemae <img alt="Run test" src="https://github.com/motohidentaku/yoiotemae/workflows/CI/badge.svg"></a>
よいお点前
「・・・　IoT ・・・」の略称（略称は検討中）

複数のセンサーを接続したRasberryPiを対象としたIoT-PFのテンプレート

## Requirements

* Raspberry Pi Zero W
* Python 3.7
* [Poetry](https://python-poetry.org/) 

## Install
Poetry
```
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
$ source $HOME/.poetry/env
```
下記のバージョン確認で`・・・py2.7/subprocess32.py:149: RuntimeWarning: The _posixsubprocess・・・`というエラーが出たら、`~/.poetry/bin/poetry`の１行目を`#!/usr/bin/env python3`に変更
```
$ poetry --version
```

## 想定環境
複数のRasberryPiがあり、それぞれのRasberryPiには複数のセンサ（温度、湿度、照度　等）がついている。
ただし、個々のRasberryPiに接続されているセンサーは異なることがある。
（温度センサのみが接続されているRasberryPiもあれば、温度、湿度、照度の3つのセンサがついているRasberryPiもある）

## 実施したいこと
RasberryPiのセンサから取得できる情報をサーバに送信したい

## このyoiotemaeで実施したいこと
- 設定ファイルを編集することで、どのセンサが接続されているか管理できる
- 設定ファイルを編集することで、センサから情報を取得する際のパラメータを管理できる
- 設定ファイルにサーバ送信に関するパラメータを管理できる
- センサの種類は今後も増えていくので、独立したモジュールとして構築したい

## 現段階の実現方式
- 設定ファイルをconfig/para.configに設置
- lib配下に各センサに対応するpyファイルを作成し、共通メソッドとして、インスタンス生成時に
パラメータ（複数の可能性あり）を受け取り、getメソッドによりセンサからの情報（服須の可能性あり）を取得できる仕様とする
- メインとなるmain.pyは、設定ファイルに基づき、必要なモジュールを動的に読み込み、センサからの情報を取得し、
設定ファイルに基づいいてサーバに送信するjsonを生成する

## 改善希望点
