import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, transforms
import matplotlib.pyplot as plt
from PIL import Image

class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle_boot']

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.3),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.3),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 7 * 7, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 10)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Running on {device}")

model = CNN().to(device)
model.load_state_dict(torch.load("./unit_03/fmnist.pth", weights_only=True))
model.eval()

def predict(img_path, model):
    if img_path == None:
        raise Exception("image path is required")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28, 28)),
    ])

    image = Image.open(img_path).convert('L')
    image = transform(image).unsqueeze(0).to(device)

    with torch.inference_mode():
        output = model(image)
        class_name = class_names[torch.argmax(output).item()]
        print(f"Predicted class: {class_name}")

        return class_name

# if __name__ == "__main__":
#     img_path = "./fmnist_samples/7_Sneaker.png"
#     predict(img_path, model)