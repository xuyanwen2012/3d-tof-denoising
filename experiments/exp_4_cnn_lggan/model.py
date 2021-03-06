#!/usr/bin/env python

import torch
import torch.nn as nn

"""
Idea is to use two different models, the first model predicting the lighting and other parameters from the input image; and the second model predicting True Depth Map using parameters from first model along with False Depth Map.

Model A
=======

Input  : False Depth Map
Output : Light Position, Camera Position, Material Properties

Model B
=======

Input  : False Depth Map, Output of Model A
Output : True Depth Map 

"""

class Model_A(nn.Module):
    def __init__(self, config):
        super(Model_A, self).__init__()
        self.config = config
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(16),            
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(32),            
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(32),            
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer4 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(64),            
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer5 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(64),            
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(in_features=53*64*64, out_features=self.config.data.parameters.light_params)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

class Generator(nn.Module):
    def __init__(self, config):
        super(Model_B, self).__init__()
        self.config = config
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(16))
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(32))
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=2, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(32))
        self.layer4 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=32, out_channels=32, kernel_size=5, stride=2, padding=2, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32))
        self.layer5 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=32, out_channels=16, kernel_size=5, stride=2, padding=2,output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(16))
        self.layer6 = nn.Sequential(
            nn.ConvTranspose2d(in_channels=16, out_channels=1, kernel_size=5, stride=2, padding=2, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(1))

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        return out

class LocalDiscriminator(nn.Module):
    def __init__(self, config):
        self.config = config

    def forward(self, x):
        pass

class GlobalDiscriminator(nn.Module):
    def __init__(self, config):
        self.config = config

    def forward(self, x):
        pass

class Concatenator(nn.Module):
    def __init__(self, config):
        pass

    def forward(self, x):
        pass