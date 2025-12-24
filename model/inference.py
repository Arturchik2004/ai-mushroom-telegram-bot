import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import os
import io

class MushroomPredictor:
    def __init__(self, model_path='model/mushroom_model.pth', config_path='model/config.json'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🧠 Загружаю модель на {self.device}...")
        
        # 1. Загружаем классы
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Нет файла {config_path}")
        with open(config_path, 'r') as f:
            self.classes = json.load(f)

        # 2. Архитектура модели
        self.model = models.efficientnet_b0(weights=None)
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_ftrs, len(self.classes))
        
        # 3. Веса
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Нет файла {model_path}")
            
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()
        
        # 4. Трансформации
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_input):
        """
        image_input: может быть путем к файлу (str) ИЛИ байтовым потоком (io.BytesIO)
        """
        # PIL.Image.open отлично открывает и пути, и байтовые потоки
        image = Image.open(image_input).convert('RGB')
        
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            top_p, top_class_idx = probs.topk(1, dim=1)
            
            return self.classes[top_class_idx.item()], top_p.item()