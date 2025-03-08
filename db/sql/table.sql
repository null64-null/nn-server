CREATE TABLE models (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    discription TEXT,
    nn BYTEA NOT NULL,  -- バイナリ形式でモデル保存
    learning_history JSONB NOT NULL, -- 学習履歴
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE learning_requests (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    discription TEXT,
    model_orders JSONB NOT NULL,
    criterion_order TEXT NOT NULL,
    tokens_length INTEGER NOT NULL,
    num_epochs INTEGER NOT NULL,
    batch_size INTEGER NOT NULL,
    train_data_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 編集不可
CREATE TABLE learning_data (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    discription TEXT,
    feature TEXT,
    first_text_order TEXT,
    second_text_order TEXT,
    option_order TEXT,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

