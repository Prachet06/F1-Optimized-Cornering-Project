# TODO: Create a bespoke CNN model for this data set
# TODO: Think about cropping the image to only include the road maybe but I guess the image has to be square
# TODO: Think of how much padding should be applied to this CNN based on how important the borders of the image are
#       consult this article (https://medium.com/thedeephub/convolutional-neural-networks-a-comprehensive-guide-5cc0b5eae175)
#       and think about the stride too.
# TODO: Will probably need to add padding 
# import tensorflow as tf


# from tensorflow.keras import datasets, layers, models
# import matplotlib.pyplot as plt

# TODO: Choose a method to normalize the data you have which is helpful for YOUR data

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models
from torchvision.models import ResNet18_Weights

data_dir = "../Data/cnn-classes"
batch_size = 16
num_epochs = 10
learning_rate = 1e-4
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15
seed = 42

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

weights = ResNet18_Weights.DEFAULT

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=weights.transforms().mean,
        std=weights.transforms().std
    )
])

eval_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=weights.transforms().mean,
        std=weights.transforms().std
    )
])

full_dataset = datasets.ImageFolder(root=data_dir)
print("Classes:", full_dataset.classes)
print("Total images:", len(full_dataset))

total_size = len(full_dataset)
train_size = int(train_ratio * total_size)
val_size = int(val_ratio * total_size)
test_size = total_size - train_size - val_size

generator = torch.Generator().manual_seed(seed)

train_subset, val_subset, test_subset = random_split(
    full_dataset,
    [train_size, val_size, test_size],
    generator=generator
)

train_subset.dataset = datasets.ImageFolder(root=data_dir, transform=train_transform)
val_subset.dataset = datasets.ImageFolder(root=data_dir, transform=eval_transform)
test_subset.dataset = datasets.ImageFolder(root=data_dir, transform=eval_transform)

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True, num_workers=0)
val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=0)
test_loader = DataLoader(test_subset, batch_size=batch_size, shuffle=False, num_workers=0)

model = models.resnet18(weights=weights)
model.fc = nn.Linear(model.fc.in_features, len(full_dataset.classes))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

def run_epoch(model, loader, criterion, optimizer=None):
    if optimizer is None:
        model.eval()
    else:
        model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.set_grad_enabled(optimizer is not None):
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)

            if optimizer is not None:
                optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            if optimizer is not None:
                loss.backward()
                optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    return running_loss / total, correct / total

best_val_acc = 0.0
best_model_path = "best_resnet18.pth"

for epoch in range(num_epochs):
    train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer)
    val_loss, val_acc = run_epoch(model, val_loader, criterion)

    print(
        f"Epoch {epoch+1}/{num_epochs} | "
        f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
        f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}"
    )

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), best_model_path)

print("Best validation accuracy:", best_val_acc)

model.load_state_dict(torch.load(best_model_path, map_location=device))
test_loss, test_acc = run_epoch(model, test_loader, criterion)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")