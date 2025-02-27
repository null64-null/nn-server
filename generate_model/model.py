import torch.nn as nn

'''
def layerSelector(orders, input_size):
  layers = []

  for order in orders:
    if order["type"] == "Linear":
        layers.append(nn.Linear(input_size, order["nodes"]))
        input_size = order["nodes"]
    if order["type"] == "ReLU":
        layers.append(nn.ReLU())
    if order["type"] == "Sigmoid":
        layers.append(nn.Sigmoid())

  return nn.Sequential(*layers)
'''
def layerSelector(orders, input_size):
  layers = []

  for order in orders:
    if order.type == "Linear":
        layers.append(nn.Linear(input_size, order.nodes))
        input_size = order.nodes
    if order.type == "ReLU":
        layers.append(nn.ReLU())
    if order.type == "Sigmoid":
        layers.append(nn.Sigmoid())

  return nn.Sequential(*layers)

class CustomNN(nn.Module):
    def __init__(self, input_size, orders):
        super(CustomNN, self).__init__()
        self.layers = layerSelector(orders, input_size)

    def forward(self, x):
        return self.layers(x)