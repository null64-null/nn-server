import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from generate_model.model import CustomNN
from generate_model.criterion import criterionSelector
import json

# ネットワーク定義
'''
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size2, output_size)
        self.sigmoid = nn.Sigmoid()  # 出力層

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x
'''
    
# 1ステップ分の学習を行う
def train_step(model, criterion, optimizer, inputs, labels):
    # 順伝搬
    outputs = model(inputs) #outputsは多分model情報も込み（modelはnnライブラリメソッド）
    
    # 損失計算
    loss = criterion(outputs, labels) #lossは多分model情報も込み（criterionはnnライブラリメソッド）
    
    # 勾配初期化 & 逆伝搬
    optimizer.zero_grad() #optimizerはmodelを引数であらかじめ取り込んでいる
    loss.backward() #多分lossにmodel情報があるので、逆伝搬が計算できる、ここでmodelに勾配情報を伝えている
    
    # パラメータ更新
    optimizer.step() #modelに伝えられた勾配情報を元にパラメータを更新
    
    # 損失を返す(損失以外は返さない)
    return loss.item()

# 指定したエポック数だけ学習を繰り返す
def train(model, dataloader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        total_loss = 0
        for inputs, labels in dataloader:
            loss = train_step(model, criterion, optimizer, inputs, labels)
            total_loss += loss
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss / len(dataloader):.4f}')


def generate_model(input_size, model_orders, criterion_order, num_epochs, batch_size, inputs, labels):
    # モデル設定
    model = CustomNN(input_size, model_orders)

    # 損失関数と最適化手法
    criterion = criterionSelector(criterion_order)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    
    # データローダー
    dataset = TensorDataset(inputs, labels)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # 学習実行
    train(model, dataloader, criterion, optimizer, num_epochs)

    #state_dict = model.state_dict()
    #torch.save(state_dict, 'model.pth')
    #print(state_dict.keys())
    #return state_dict

    return model