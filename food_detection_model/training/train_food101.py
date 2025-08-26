import os, json, argparse
import torch
from torchvision import models, transforms, datasets
from torch.utils.data import DataLoader
import torch.nn as nn, torch.optim as optim

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True, help='root data dir for Food-101')
parser.add_argument('--out', default='../models/food_model.pth')
parser.add_argument('--epochs', type=int, default=8)
parser.add_argument('--batch', type=int, default=32)
parser.add_argument('--lr', type=float, default=1e-3)
args = parser.parse_args()

data_dir = args.data
train_tf = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])
val_tf = transforms.Compose([
    transforms.Resize(256), transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

train_ds = datasets.ImageFolder(os.path.join(data_dir, 'train'), transform=train_tf)
val_ds = datasets.ImageFolder(os.path.join(data_dir, 'val'), transform=val_tf)
train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=4)
val_loader = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=4)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(train_ds.classes))
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=args.lr)

best_acc = 0.0
for epoch in range(args.epochs):
    model.train()
    running_loss = 0.0
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * imgs.size(0)
    # val
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    acc = correct / total
    print(f"Epoch {epoch+1}/{args.epochs} val_acc={acc:.4f}")
    if acc > best_acc:
        best_acc = acc
        out_path = os.path.join(os.path.dirname(__file__), args.out)
        print("Saving best model to", out_path)
        torch.save({'model_state': model.state_dict(), 'class_map': {str(i): c for i,c in enumerate(train_ds.classes)}}, out_path)
print("Done. Best val acc:", best_acc)