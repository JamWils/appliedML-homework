from torchvision import datasets
from torchvision.transforms import ToTensor
from PIL import Image
import os

test_data = datasets.FashionMNIST(root="data", train=False, download=True, transform=ToTensor())

class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle_boot']

# Create output folder
os.makedirs("fmnist_samples", exist_ok=True)

# Save one sample per class
saved_classes = set()
for img, label in test_data:
    if label not in saved_classes:
        # Convert tensor to PIL Image
        pil_img = Image.fromarray((img.squeeze().numpy() * 255).astype('uint8'))
        pil_img.save(f"fmnist_samples/{label}_{class_names[label]}.png")
        saved_classes.add(label)
    if len(saved_classes) == 10:
        break

print("Saved 10 sample images to fmnist_samples/")