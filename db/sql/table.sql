CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nn BYTEA,  -- バイナリ形式でモデル保存
    learning_history: JSONB, -- 学習履歴
);

CREATE TABLE learning_requests (
    id TEXT PRIMARY KEY,
    input_size INTEGER NOT NULL,
    model_orders JSONB NOT NULL,
    criterion_order TEXT NOT NULL,
    num_epochs INTEGER NOT NULL,
    batch_size INTEGER NOT NULL,
    train_data_id TEXT NOT NULL,
    test_data_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 編集不可
CREATE TABLE learning_data (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB NOT NULL
);

