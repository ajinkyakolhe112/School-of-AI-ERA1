#!/usr/bin/env python3

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
#!pip install torchsummary
from torchsummary import summary

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
device

#%%
batch_size = 1024

train_loader = torch.utils.data.DataLoader(
	datasets.MNIST('../data', train=True, download=True,
					transform=transforms.Compose([
						transforms.ToTensor(),
						transforms.Normalize((0.1307,), (0.3081,))
					])),
	batch_size=batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(
	datasets.MNIST('../data', train=False, transform=transforms.Compose([
						transforms.ToTensor(),
						transforms.Normalize((0.1307,), (0.3081,))
					])),
	batch_size=batch_size, shuffle=True)

#%%
from tqdm import tqdm
pbar = tqdm(train_loader)

for batch_idx, (data, target) in enumerate(pbar):
	data, target = data.to(device), target.to(device)
	print("One Batch Ends")

#%%
class FirstDNN(nn.Module):
	def __init__(self):
		super(FirstDNN, self).__init__()
		# r_in:1, n_in:28, j_in:1, s:1, r_out:3, n_out:28, j_out:1
		self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.pool1 = nn.MaxPool2d(2, 2)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv4 = nn.Conv2d(128, 256, 3, padding = 1)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.pool2 = nn.MaxPool2d(2, 2)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv5 = nn.Conv2d(256, 512, 3)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv6 = nn.Conv2d(512, 1024, 3)
		# r_in: , n_in: , j_in: , s: , r_out: , n_out: , j_out:
		self.conv7 = nn.Conv2d(1024, 10, 3)
# Correct values
# https://user-images.githubusercontent.com/498461/238034116-7db4cec0-7738-42df-8b67-afa971428d39.png
	def forward(self, x):
		x = self.pool1(F.relu(self.conv2(F.relu(self.conv1(x)))))
		x = self.pool2(F.relu(self.conv4(F.relu(self.conv3(x)))))
		x = F.relu(self.conv6(F.relu(self.conv5(x))))
		x = F.relu(self.conv7(x)) #<< Correct answer is to remove the ReLU from here
		x = x.view(-1, 10)
		return F.log_softmax(x)

#%%
model = FirstDNN().to(device)
summary(model, input_size=(1, 28, 28))

#%%
from tqdm import tqdm
def train(model, device, train_loader, optimizer, epoch):
	model.train()
	pbar = tqdm(train_loader)
	for batch_idx, (data, target) in enumerate(pbar):
		data, target = data.to(device), target.to(device)
		optimizer.zero_grad()
		output = model(data)
		loss = F.nll_loss(output, target)
		loss.backward()
		optimizer.step()
		pbar.set_description(desc= f'loss={loss.item()} batch_id={batch_idx}')
		
		
def test(model, device, test_loader):
	model.eval()
	test_loss = 0
	correct = 0
	with torch.no_grad():
		for data, target in test_loader:
			data, target = data.to(device), target.to(device)
			output = model(data)
			test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
			pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
			correct += pred.eq(target.view_as(pred)).sum().item()
			
	test_loss /= len(test_loader.dataset)
	
	print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
		test_loss, correct, len(test_loader.dataset),
		100. * correct / len(test_loader.dataset)))
	
#%%
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

for epoch in range(1, 2):
	train(model, device, train_loader, optimizer, epoch)
	test(model, device, test_loader)