CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nn BYTEA,  -- バイナリ形式でモデル保存
    learning_history: JSONB, -- 学習履歴
);

CREATE TABLE learning_orders (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    learning_order JSONB NOT NULL
);

-- 編集不可
CREATE TABLE learning_data (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB NOT NULL
);

