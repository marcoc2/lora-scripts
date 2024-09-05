import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import os
import numpy as np
import torch

# Pipeline de transformações modificado
transform = A.Compose([
    A.OneOf([
        A.RandomRotate90(),
        A.Rotate(limit=45, p=0.5),
    ], p=0.6),
    A.Flip(p=0.5),
    A.Transpose(p=0.5),
    A.OneOf([
        A.MotionBlur(p=0.2),
        A.MedianBlur(blur_limit=3, p=0.1),
        A.Blur(blur_limit=3, p=0.1),
    ], p=0.3),
    A.OneOf([
        A.OpticalDistortion(p=0.3),
        A.GridDistortion(p=0.1),
        A.ElasticTransform(p=0.3),
    ], p=0.2),
    A.OneOf([
        A.CLAHE(clip_limit=2),
        A.Emboss(),
        A.RandomBrightnessContrast(),
    ], p=0.3),
    A.HueSaturationValue(p=0.3),
    A.RGBShift(p=0.3),
    A.RandomGamma(p=0.2),
    A.CoarseDropout(max_holes=8, max_height=64, max_width=64, min_holes=1, min_height=32, min_width=32, fill_value=0, p=0.3),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.5),
    A.RandomSizedCrop(min_max_height=(300, 427), height=427, width=640, p=0.5),
    A.Resize(height=512, width=512),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

def augment_and_save(image_path, output_dir, transform, num_augmented_images=5):
    # Carrega a imagem com OpenCV (BGR)
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return
    
    # Converte BGR para RGB (necessário para Albumentations)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    filename = os.path.basename(image_path).split('.')[0]
    for i in range(num_augmented_images):
        # Aplica as transformações e converte para tensor
        augmented = transform(image=image)['image']
        
        # Converte o tensor de volta para NumPy array e reverte a normalização
        augmented = augmented.permute(1, 2, 0).cpu().numpy()  # De volta para [H, W, C]
        
        # Reverte a normalização
        augmented = augmented * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])
        augmented = np.clip(augmented, 0, 1)

        # Converte para [0, 255] e para uint8 para salvar corretamente
        augmented = (augmented * 255).astype(np.uint8)
        
        # Converte RGB de volta para BGR para salvar com OpenCV
        augmented = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)
        
        output_path = os.path.join(output_dir, f"{filename}_aug_{i}.jpg")
        cv2.imwrite(output_path, augmented)  # Salva a imagem

# O resto do código permanece o mesmo
input_dir = '.'
output_dir = './augmentadas'
os.makedirs(output_dir, exist_ok=True)

valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

for filename in os.listdir(input_dir):
    if any(filename.lower().endswith(ext) for ext in valid_extensions):
        image_path = os.path.join(input_dir, filename)
        augment_and_save(image_path, output_dir, transform)
    else:
        print(f"Ignorando arquivo não suportado: {filename}")