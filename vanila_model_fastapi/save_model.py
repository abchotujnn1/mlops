#save model.py
import torch
import torch.nn as nn

class DemoModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(10, 1)
    def forward(self, x):
        return self.lin(x)


model = DemoModel()
#train
scripted = torch.jit.script(model)
scripted.save("model.pt")