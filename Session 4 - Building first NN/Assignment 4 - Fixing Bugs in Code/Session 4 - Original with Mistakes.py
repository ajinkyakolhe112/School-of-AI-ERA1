import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

#%%
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
device
# Train data transformations
train_transforms = transforms.Compose([
	transforms.RandomApply([transforms.CenterCrop(22), ], p=0.1),
	transforms.Resize((28, 28)),
	transforms.RandomRotation((-15., 15.), fill=0),
	transforms.ToTensor(),
	transforms.Normalize((0.1307,), (0.3081,)),
	])

# Test data transformations
test_transforms = transforms.Compose([
	transforms.ToTensor(),
	transforms.Normalize((0.1407,), (0.4081,))
	])
	
train_data = datasets.MNIST('../data', train=True, download=True, transform=train_transforms)
test_data = datasets.MNIST('../data', train=True, download=True, transform=train_transforms)

#%%
batch_size = 512
kwargs = {'batch_size': batch_size, 'shuffle': False, 'pin_memory': True} #FixME: spec error on coderunner 4. works fine on colab
test_loader = torch.utils.data.DataLoader(train_data, **kwargs)
train_loader = torch.utils.data.DataLoader(train_data, **kwargs)

#%%
"""
import matplotlib.pyplot as plt
batch_data, batch_label = next(iter(train_loader)) 
fig = plt.figure()
for i in range(12):
	plt.subplot(3,4,i+1)
	plt.tight_layout()
	plt.imshow(batch_data[i].squeeze(0), cmap='gray')
	plt.title(batch_label[i].item())
	plt.xticks([])
	plt.yticks([])
"""
#%%
class Net(nn.Module):
	#This defines the structure of the NN.
	def __init__(self):
		super(Net, self).__init__()
		self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
		self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
		self.conv3 = nn.Conv2d(64, 128, kernel_size=3)
		self.conv4 = nn.Conv2d(128, 256, kernel_size=3)
		self.fc1 = nn.Linear(320, 50)
		self.fc2 = nn.Linear(50, 10)
		
	def forward(self, x):
		x = F.relu(self.conv1(x), 2)
		x = F.relu(F.max_pool2d(self.conv2(x), 2)) 
		x = F.relu(self.conv3(x), 2)
		x = F.relu(F.max_pool2d(self.conv4(x), 2)) 
		x = x.view(-1, 320)
		x = F.relu(self.fc1(x))
		x = self.fc2(x)
		return F.log_softmax(x, dim=1)

#%%
# Data to plot accuracy and loss graphs
train_losses = []
test_losses = []
train_acc = []
test_acc = []

test_incorrect_pred = {'images': [], 'ground_truths': [], 'predicted_vals': []}

#%%

from tqdm import tqdm

def GetCorrectPredCount(pPrediction, pLabels):
	return pPrediction.argmax(dim=1).eq(pLabels).sum().item()

def train(model, device, train_loader, optimizer):
	model.train()
	pbar = tqdm(train_loader)
	
	train_loss = 0
	correct = 0
	processed = 0
	
	for batch_idx, (data, target) in enumerate(pbar):
		data, target = data.to(device), target.to(device)
		optimizer.zero_grad()
		
		# Predict
		pred = model(data)
		
		# Calculate loss
		loss = F.nll_loss(pred, target)
		train_loss+=loss.item()
		
		# Backpropagation
		loss.backward()
		optimizer.step()
		
		correct += GetCorrectPredCount(pred, target)
		processed += len(data)
		
		pbar.set_description(desc= f'Train: Loss={loss.item():0.4f} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}')
		
	train_acc.append(100*correct/processed)
	train_losses.append(train_loss/len(train_loader))
	
def test(model, device, test_loader):
	model.eval()

	test_loss = 0
	correct = 0

	with torch.no_grad():
		for batch_idx, (data, target) in enumerate(test_loader):
			data, target = data.to(device), target.to(device)
		
			output = model(data)
			test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
		
			correct += GetCorrectPredCount(output, target)
				
				
	test_loss /= len(test_loader.dataset)
	test_acc.append(100. * correct / len(test_loader.dataset))
	test_losses.append(test_loss)

	print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
			test_loss, correct, len(test_loader.dataset),
			100. * correct / len(test_loader.dataset)))

#%%
model = Net().to(device)
optimizer = optim.SGD(model.parameters(), lr=10.01, momentum=0.9)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.1, verbose=True)
num_epochs = 20

for epoch in range(1, num_epochs+1):
	print(f'Epoch {epoch}')
	train(model, device, train_loader, optimizer)
	test(model, device, train_loader)
	scheduler.step()
	
	if epoch == 3:
		break
	
#%%
fig, axs = plt.subplots(2,2,figsize=(15,10))
axs[0, 0].plot(train_losses)
axs[0, 0].set_title("Training Loss")
axs[1, 0].plot(train_acc)
axs[1, 0].set_title("Training Accuracy")
axs[0, 1].plot(test_losses)
axs[0, 1].set_title("Test Loss")
axs[1, 1].plot(test_acc)
axs[1, 1].set_title("Test Accuracy")

#%%
#!pip install torchsummary
from torchsummary import summary
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
model = Net().to(device)
summary(model, input_size=(1, 28, 28))