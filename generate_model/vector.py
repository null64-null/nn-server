import torch
from transformers import BertModel, BertTokenizer
from db.learning_data_query import Relevance ,Score ,LearningData

# ライブラリ導入
tokenizer = BertTokenizer.from_pretrained("cl-tohoku/bert-base-japanese")
model = BertModel.from_pretrained("cl-tohoku/bert-base-japanese")

def vectorize_text(text, max_length=64):
    # テキストをトークン化、ID化 
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,  # [CLS] と [SEP] トークンを追加
        max_length=max_length,  # 最大長を指定
        padding='max_length',  # 最大長にパディング
        truncation=True,  # 長すぎる場合は切り捨て
        return_tensors='pt'  # PyTorchのテンソルとして返す
    )

    # BERTの埋め込みを取得
    with torch.no_grad():
        outputs = model(**encoding)

    # 埋め込み（最後の隠れ層）
    embeddings = outputs.last_hidden_state

    return embeddings

def vectorize_texts(texts):
    vectors = []
    for text in texts:
        vector = vectorize_text(text)
        vector = vector.squeeze(0).mean(dim=0) #最初の次元を捨てトークンごとの平均を取る
        vectors.append(vector)
    
    return torch.stack(vectors)
    
def divide_input(learning_data: LearningData):
    texts = []
    scores = []
    
    for item in learning_data.data:
        if isinstance(item, Score):
            texts.append(item.text)
            scores.append(item.score)
        elif isinstance(item, Relevance):
            # Relevanceの場合、QとDを結合してテキストとして扱う
            combined_text = f"{item.Q} {item.D}"
            texts.append(combined_text)
            scores.append(item.score)
        else:
            raise ValueError(f"Unexpected data type: {type(item)}")

    return texts, scores

def make_vectorized_data_set(learning_data: LearningData):
    texts, scores = divide_input(learning_data)

    score_tensor = torch.tensor(scores, dtype=torch.float32)
    text_tensor = vectorize_texts(texts)

    print(text_tensor.shape)
    print(score_tensor.shape)

    return text_tensor, score_tensor


