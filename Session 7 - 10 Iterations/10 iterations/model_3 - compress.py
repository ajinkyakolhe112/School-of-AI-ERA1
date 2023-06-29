import torch.nn as nn
import torch.nn.functional as F

import torch.nn as nn
import torch.nn.functional as F

class Model_3(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv0 = nn.Conv2d(1,10, 3, padding=1)    # 28 -> 28 | 3
        
        # Block 1
        self.block1 = nn.ModuleDict({
            "conv1": nn.Conv2d(10, 10, 3, padding=1),
            "relu1" : nn.ReLU(),
            "conv2": nn.Conv2d(10, 20, 3, padding=1),
            "relu2" : nn.ReLU(),
        })

        # Maxpooling before or after 1x1 convolution?
        self.transition1 = nn.Sequential(
            nn.MaxPool2d(2, 2),
            nn.Conv2d(20,10,1), # Squeeze
        )

        # Block 2
        self.block2 = nn.ModuleDict({
            "conv1": nn.Conv2d(10, 10, 3, padding=1),
            "relu1" : nn.ReLU(),
            "conv2": nn.Conv2d(10, 20, 3, padding=1),
            "relu2" : nn.ReLU(),
        })
        
        self.transition2 = nn.Sequential(
            nn.MaxPool2d(2, 2),
            nn.Conv2d(20,10,1), # Squeeze
        )

        # Block 3
        self.block3 = nn.ModuleDict({
            "conv1": nn.Conv2d(10, 10, 3, padding=1),
            "relu1" : nn.ReLU(),
            "conv2": nn.Conv2d(10, 20, 3, padding=1),
            "relu2" : nn.ReLU(),
        })

        self.transition3 = nn.Sequential(
            nn.MaxPool2d(2, 2),
            nn.Conv2d(20,10,1), # Squeeze
        )

        # Block 4
        self.block4 = nn.ModuleDict({
            "conv7": nn.Conv2d(10, 10, 3),
        })

    def forward(self, x):
        b1, b2, b3, b4 = self.block1, self.block2, self.block3, self.block4

        x = self.conv0(x)

        x = b1.relu2(b1.conv2(b1.relu1(b1.conv1(x))))
        x = self.transition1(x)
        
        x = b2.relu2(b2.conv2(b2.relu1(b2.conv1(x))))
        x = self.transition2(x)
        
        x = b3.relu2(b3.conv2(b3.relu1(b3.conv1(x))))
        x = self.transition3(x)

        x = b4.conv7(x)

        # (-1 = dim 0, 10 = dim 1)
        x = x.view(-1, 10)

        output = F.log_softmax(x, dim=1)
        probs = F.softmax(x, dim=1)
        return output

if __name__=="__main__":
    from torchsummary import summary

    model_3 = Model_3()
    summary(model_3,input_size=(1,28,28))

    for name in model_3.state_dict():
        print(name)
    
    # for module in model_3.modules():
        # print(module)

    

        


