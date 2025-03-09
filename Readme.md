# NN Server (API)

## 概要

## API 仕様

### モデル (models)
ニューラルネットワークモデルに関するエンドポイント

- POST /create_model
  - ニューラルネットワークモデルを生成し、保存する
  - リクエストの学習リクエスト（learning_request）に応じて、実際にサーバー内で学習が行われる
  - 学習には、DBに保存されている指定の学習データ（learning_data）を用いる
  - 既存のidに対するリクエストの場合、学習結果でそのidを持つモデルを更新する（PUTを兼ねる）

- GET /get_all_model_ids
  - id等のみ、全件取得する
  - 取得するものは以下
    - id
    - name
    - discription 

- GET /get_model
  - 指定したidのモデルを1件取得する 
  - モデルのバイナリデータ以外の全カラムを取得

- DELETE /delete_model
  - 指定したidのモデルを1件削除する

### 学習リクエスト (learning_request)
学習の詳細設定（学習リクエスト）に関するエンドポイント

- POST /save_learninig_request
  - 学習リクエストを保存する

- PUT /update_learninig_request
  - 学習リクエストの内容を更新する

- DELETE /delete_learninig_request
  - 指定したidの学習リクエストを削除する

- GET /get_all_learning_request_ids
  - id等のみ、全件取得する
  - 取得するものは以下
    - id
    - name
    - discription 

- GET /get_learning_request
  - 指定したidのモデルを1件取得する 
  - 全カラムを取得

### 学習データ (learning_data)
学習に用いるデータに関するエンドポイント<br>
更新（PUT）は設けない

- POST /create_learning_data
  - 学習のためのデータを生成し、保存する
  - 学習データはGroqAPIを仕様して生成する
  - GroqAPIに投げるプロンプトを生成する処理あり

- DELETE /delete_learning_data
  - 指定したidの学習データを削除する

- GET /get_all_learning_data_ids
  - id等のみ、全件取得する
  - 取得するものは以下
    - id
    - name
    - discription 

- GET /get_learning_data
  - 指定したidの学習データを1件取得する
  - 全カラムを取得

### 推論 (inference)
推論に関するエンドポイント
- POST /inference
  - 推論を行う
  - DBに保存されている学習済みモデルを使用する
  - 推論結果を返却する

