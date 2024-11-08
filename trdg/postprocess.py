import os
from PIL import Image, ImageDraw, ImageFont

def create_annotations_for_trdg_images(image_dir, label_dir, font_path="./fonts/latin/Roboto-Italic.ttf"):
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
    
    image_files = [f for f in os.listdir(image_dir) if f.endswith(".jpg") or f.endswith(".png")]
    image_files.sort()

    for i, img_filename in enumerate(image_files):
        img_path = os.path.join(image_dir, img_filename)
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        text = img_filename.split("_")[0]  # Assuming the text is part of the filename
        
        font = ImageFont.truetype(font_path, 32)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        bbox = (10, 10, 10 + text_width, 10 + text_height)  # Example bounding box
        
        new_img_name = f"img_trdg_{i:04d}.png"
        new_lbl_name = f"img_trdg_{i:04d}.txt"

        os.rename(img_path, os.path.join(image_dir, new_img_name))
        
        label_path = os.path.join(label_dir, new_lbl_name)
        with open(label_path, "w") as f:
            f.write(f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[1]},{bbox[2]},{bbox[3]},{bbox[0]},{bbox[3]},\"\"\n")

# Example usage
create_annotations_for_trdg_images(image_dir="./trdg_output", label_dir="./trdg_output/labels")