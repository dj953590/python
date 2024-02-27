import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple neural network with ReLU activation
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Set random seed for reproducibility
torch.manual_seed(42)

# Input size, hidden size, and output size
input_size = 10
hidden_size = 5
output_size = 2

# Instantiate the model
model = MyModel()

# Define a sample input
sample_input = torch.rand((1, input_size))

# Forward pass through the model
output = model(sample_input)

print("Sample Input:")
print(sample_input)
print("\nOutput after ReLU activation:")
print(output)