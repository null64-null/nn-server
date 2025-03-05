# NN Server (API)

## API 仕様

### モデル (models)

#### POST /create_model

ニューラルネットワークモデルを生成し、保存します。学習リクエストの内容に基づいて新しいモデルを作成するか、既存のモデルを更新します。

#### GET /get_all_model_ids

保存されているすべてのモデルの ID リストを取得します。

#### GET /get_model

指定された ID のモデル情報を取得します。モデルの設定情報と学習履歴を含みます（モデルのバイナリデータは除く）。

#### DELETE /delete_model

指定された ID のモデルを削除します。

### 学習リクエスト (learning_request)

#### POST /save_learninig_request

新しい学習リクエストを保存します。モデルの構造、学習パラメータ、使用するデータセットなどの設定を含みます。

#### PUT /update_learninig_request

既存の学習リクエストの内容を更新します。モデル構造や学習パラメータの変更が可能です。

#### DELETE /delete_learninig_request

指定された ID の学習リクエストを削除します。

#### GET /get_all_learning_request_ids

保存されているすべての学習リクエストの ID リストを取得します。

#### GET /get_learning_request

指定された ID の学習リクエストの詳細情報を取得します。

### 学習データ (learning_data)

#### POST /create_learning_data

AI を使用して新しい学習データを生成し、保存します。特徴量の生成やテキストの関連性評価などのデータを作成できます。

#### DELETE /delete_learning_data

指定された ID の学習データを削除します。

#### GET /get_all_learning_data_ids

保存されているすべての学習データの ID リストを取得します。

#### GET /get_learning_data

指定された ID の学習データの内容を取得します。
