import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

torch

torch.tensor(1)

torch.ones(1,1,1)

torch.tensor(77).ndim

torch.Tensor(7).ndim

torch.Tensor(5)

torch.tensor([3,3])

torch.tensor([1,2,3,5,5]).ndim

torch.Tensor(2,10,3).ndim

# Tensor
TENSOR = torch.tensor([[[1, 2, 3],
                        [3, 6, 9],
                        [2, 4, 5]]])
TENSOR

TENSOR.shape

TENSOR

TENSOR[0]

tensor3d = torch.rand((2,4,3))

tensor3d.ndim

torch.SymInt(3)+ torch.SymInt(4)

torch.randn((3,3))

torch.zeros(3)

torch.range(0,10,2)

for i in range(0,10,2):
  print(i)

# Commented out IPython magic to ensure Python compatibility.
# %time torch.arange(0,10,2)

# Commented out IPython magic to ensure Python compatibility.
# %timeit torch.arange(0,10,2)

import sys

sys.getsizeof(torch.tensor(3))

torch.tensor(3).nbytes

torch.tensor(3).size

tensor = torch.tensor(3)

tensor.shape,tensor.dtype,tensor.ndim,tensor.device

vars(tensor)

dir(tensor)

tensor3d[0].view()

tensor3d.size()

tensor3d.shape

tensor3d

tensor3d(axis=0)

import torch

torch.tensor(1)

torch.tensor(1).ndim

torch.rand((100,100,3))

