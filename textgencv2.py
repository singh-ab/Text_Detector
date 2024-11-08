import os
import random
import glob
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import albumentations as A
import math

def generate_text_snippet(text, font_path, font_size, color=(0, 0, 0), opacity=255, max_width=None, curve=False):
    if not text:
        return None
    
    font = ImageFont.truetype(font_path, font_size)
    dummy_img = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    
    if curve:
        # Calculate the width and height of the curved text
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        radius = text_width // 2
        image = Image.new('RGBA', (text_width, text_height * 2), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw each character along the curved path
        angle_step = 180 / len(text)
        for i, char in enumerate(text):
            angle = angle_step * i - 90
            x = radius + radius * math.cos(math.radians(angle))
            y = radius + radius * math.sin(math.radians(angle))
            draw.text((x, y), char, font=font, fill=color + (opacity,))
    else:
        # Split text into multiple lines based on max_width
        if max_width:
            lines = []
            words = text.split()
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                text_width, _ = draw.textbbox((0, 0), test_line, font=font)[2:]
                if text_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
            text = "\n".join(lines)
        
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        image = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=color + (opacity,))
    
    return image

def overlay_text_on_background(background, text_image, position):
    background.paste(text_image, position, text_image)
    return background

def apply_transformations(image, annotations):
    # Convert image to RGB before applying transformations
    image = image.convert("RGB")
    transform = A.Compose([
        A.Rotate(limit=15, p=0.5),
        A.Perspective(scale=(0.02, 0.05), p=0.5),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
        A.MotionBlur(blur_limit=3, p=0.3),
        A.RandomBrightnessContrast(p=0.2),
        A.HueSaturationValue(p=0.2)
    ], keypoint_params=A.KeypointParams(format='xy'))
    image_np = np.array(image)
    
    # Convert bounding boxes to keypoints
    keypoints = []
    for bbox in annotations:
        x1, y1, x2, y2 = bbox
        keypoints.append((x1, y1))
        keypoints.append((x2, y1))
        keypoints.append((x2, y2))
        keypoints.append((x1, y2))
    
    transformed = transform(image=image_np, keypoints=keypoints)
    transformed_image = Image.fromarray(transformed["image"])
    transformed_keypoints = transformed["keypoints"]
    
    # Convert keypoints back to bounding boxes
    transformed_annotations = []
    for i in range(0, len(transformed_keypoints), 4):
        if i + 3 < len(transformed_keypoints):
            x1, y1 = transformed_keypoints[i]
            x2, y2 = transformed_keypoints[i + 2]
            transformed_annotations.append((x1, y1, x2, y2))
    
    # Ensure keypoints are within image bounds
    height, width = image_np.shape[:2]
    for j, bbox in enumerate(transformed_annotations):
        x1, y1, x2, y2 = bbox
        x1 = min(max(x1, 0), width - 1)
        y1 = min(max(y1, 0), height - 1)
        x2 = min(max(x2, 0), width - 1)
        y2 = min(max(y2, 0), height - 1)
        transformed_annotations[j] = (x1, y1, x2, y2)
    
    return transformed_image, transformed_annotations

def add_shadow(image):
    shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    shadow_width, shadow_height = image.size
    shadow_offset = random.randint(5, 20)
    draw.rectangle([shadow_offset, shadow_offset, shadow_width, shadow_height], fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    
    # Ensure both images have the same size and mode
    shadow = shadow.resize(image.size)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    image = Image.alpha_composite(shadow, image)
    return image

def add_highlight(image, position, size):
    draw = ImageDraw.Draw(image)
    draw.rectangle([position, (position[0] + size[0] * 2, position[1] + size[1] * 2)], fill=(255, 255, 0, 128))
    return image

def add_ink_bleed(image):
    return image.filter(ImageFilter.GaussianBlur(radius=2))

def add_fold_lines(image):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for _ in range(random.randint(1, 3)):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0, 128), width=2)
    return image

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def generate_synthetic_document(output_dir, num_pages=10, text_file_path="text.txt", bg_images_path="./backgrounds", font_path="./trdg/fonts/latin/Aller_Bd.ttf"):
    images_dir = os.path.join(output_dir, "images")
    labels_dir = os.path.join(output_dir, "labels")
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    text_list = read_text_file(text_file_path)
    
    print(f"Looking for background images in: {bg_images_path}")
    bg_images = glob.glob(os.path.join(bg_images_path, "*.jpg"))
    
    if not bg_images:
        raise FileNotFoundError(f"No background images found in {bg_images_path}")
    
    for page_num in range(num_pages):
        bg_image_path = random.choice(bg_images)
        print(f"Using background image: {bg_image_path}")
        bg_image = Image.open(bg_image_path).convert("RGBA")
        bg_image = bg_image.resize((2480, 3508))  # A4 size at 300 DPI
        
        draw = ImageDraw.Draw(bg_image)
        annotations = []
        
        y_position = 100
        for text in text_list:
            if not text.strip():
                continue  # Skip empty lines
            font_size = random.randint(40, 100)  # Abnormally large and small text
            if random.random() < 0.7:  # 70% chance to use black color
                color = (0, 0, 0)
            else:
                color = tuple(random.randint(0, 255) for _ in range(3))
            opacity = random.randint(128, 255)
            curve = random.random() < 0.2  # 20% chance to curve text
            text_image = generate_text_snippet(text.strip(), font_path, font_size, color=color, opacity=opacity, max_width=bg_image.width - 200, curve=curve)
            if text_image is None:
                continue
            text_width, text_height = text_image.size
            
            # Ensure text width is smaller than background width
            if text_width > bg_image.width - 200:
                text_width = bg_image.width - 200
                text_image = text_image.crop((0, 0, text_width, text_height))
            
            x_position = random.randint(100, bg_image.width - text_width - 100)
            
            # Simulate partially cut text
            if random.random() < 0.1:  # Reduced to 10% chance
                text_image = text_image.crop((0, 0, text_width // 2, text_height))
                text_width = text_width // 2
            
            bg_image = overlay_text_on_background(bg_image, text_image, (x_position, y_position))
            annotations.append((x_position, y_position, x_position + text_width, y_position + text_height))
            y_position += text_height + random.randint(20, 50)
        
        # Ensure annotations are within image bounds before transformations
        height, width = bg_image.size
        for j, bbox in enumerate(annotations):
            x1, y1, x2, y2 = bbox
            x1 = min(max(x1, 0), width - 1)
            y1 = min(max(y1, 0), height - 1)
            x2 = min(max(x2, 0), width - 1)
            y2 = min(max(y2, 0), height - 1)
            annotations[j] = (x1, y1, x2, y2)
        
        bg_image, transformed_annotations = apply_transformations(bg_image, annotations)
        bg_image = add_shadow(bg_image)
        bg_image = add_ink_bleed(bg_image)
        bg_image = add_fold_lines(bg_image)
        
        if random.random() < 0.3:
            highlight_position = (random.randint(0, bg_image.width // 2), random.randint(0, bg_image.height // 2))
            highlight_size = (random.randint(100, 300), random.randint(50, 150))
            bg_image = add_highlight(bg_image, highlight_position, highlight_size)
        
        img_filename = f"img_{page_num:04d}.jpg"  # Save as JPEG to reduce file size
        img_path = os.path.join(images_dir, img_filename)
        bg_image = bg_image.convert("RGB")  # Convert to RGB mode before saving as JPEG
        bg_image.save(img_path, format='JPEG', quality=40)
            
        # Save annotations
        label_filename = f"img_{page_num:04d}.txt"
        label_path = os.path.join(labels_dir, label_filename)
        with open(label_path, "w") as f:
            for bbox in transformed_annotations:
                f.write(f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[1]},{bbox[2]},{bbox[3]},{bbox[0]},{bbox[3]},\"\"\n")

# Example usage
generate_synthetic_document(output_dir="./dataset/", num_pages=100, text_file_path="text.txt")