import torch.nn as nn

def criterionSelector(criterion_type):
  if criterion_type == "BCE": #2クラス分類用（出力size=1限定）
    return nn.BCELoss()
  if criterion_type == "MSE": #1桁のスコア（出力size=1限定）
    return nn.MSELoss()
  if criterion_type == "CrossEntropy": #クロスエントロピー誤差
    return nn.CrossEntropyLoss()