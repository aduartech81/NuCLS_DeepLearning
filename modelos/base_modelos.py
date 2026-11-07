from torch import nn
from torchvision import models
CLASSES = ["tumor_nonMitotic", "lymphocyte", "nonTILnonMQ_stromal"]
def build(name):
 if name=='cnn_local':
  return nn.Sequential(nn.Conv2d(3,32,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),
   nn.Conv2d(32,64,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),
   nn.Conv2d(64,128,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d(1),nn.Flatten(),nn.Dropout(.3),nn.Linear(128,3))
 if name=='resnet18':
  m=models.resnet18(weights=None);m.fc=nn.Linear(m.fc.in_features,3);return m
 if name=='mobilenet_v2':
  m=models.mobilenet_v2(weights=None);m.classifier[-1]=nn.Linear(m.last_channel,3);return m
 raise ValueError(name)
