# Document Text Detection with Synthetic OCR Data

## Project Overview
This project aims to develop a text detection system capable of identifying and localizing text snippets in synthetic document images. The system generates a synthetic dataset of document-like images, applies various transformations to simulate real-world conditions, and trains a text detection model.

## Project Structure
- `textgencv2.py`: Script for generating synthetic document images with text overlays and applying transformations (PIL-based)
- `\trdg\run.py`: Script for generating synthetic document snippets with text overlays and applying transformations (TRDG)
- `\trdg\postprocess.py`: Script for postprocessing generated images
- `\trdg\images`: Background images for text overlay
- `\backgrounds`: Background images for text overlay
- `README.md`: This file.
- `\dataset`: Output directory for PIL-based dataset generator
- `\trdg\trdg_output_`: Output directory for TRDG-based dataset generator
- `\trdg\dicts`: Dictionary for overlaying text
- `documentation.md`: Detailed documentation about the project, including model choices and corner cases considered.

## Running/Using
To generate a synthetic dataset using `textgencv2.py`:
```bash
python textgencv2.py
```

Generate 500 images with random text:
```bash
py run.py -c 500 -w 5 -f 128 -b 3 -d 3 -k 15 -rk -bl 2 -rbl -tc '#000000,#888888' -na 2 --output_dir ./trdg_output
```

Generate 500 images with text from input.txt:
```bash
py run.py -i input.txt -c 500 -w 5 -f 128 -b 3 -d 3 -k 15 -rk -rbl -tc '#000000,#888888' -na 2 --output_dir ./trdg_output
```

Generate 500 images with text from input.txt:
```bash
py run.py -i input.txt -c 500 -w 5 -f 128 -b 3 -d 3 -k 15 -rk -bl 1 -rbl -tc '#000000,#888888' -na 2 --output_dir ./trdg_output --margins 10,10,10,10 --fit
```

To postprocess the generated images:
```bash
python postprocess.py
```

## Requirements
- Python 3.x
- Required libraries: `opencv-python-headless`, `Pillow`, `albumentations`, `paddleocr`

Install the required libraries using:
```bash
pip install opencv-python-headless pillow albumentations paddleocr
