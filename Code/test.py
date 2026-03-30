from torchvision import datasets

data_dir = "../Data/cnn-classes"

dataset = datasets.ImageFolder(root=data_dir)

print("Classes:", dataset.classes)
print("Class to index:", dataset.class_to_idx)
print("Total images:", len(dataset))