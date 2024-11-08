# Document Text Detection with Synthetic OCR Data

## Project Overview
This project aims to develop a text detection system capable of identifying and localizing text snippets in synthetic document images. The system generates two synthetic datasets of document-like images, applies various transformations to simulate real-world conditions, and trains a text detection model.

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

## Using the Dataset with PaddleOCR

### Step-by-Step Instructions

1. **Create the First Conda Environment**
    Create the first of two conda environments with Python 3.8:
    ```bash
    conda create --name paddleocr python=3.8
    conda activate paddleocr
    ```

2. **Download PaddlePaddle**
    Based on your GPU configuration and CUDA version, select the right version of PaddlePaddle from [this website](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/install/pip/linux-pip_en.html).
    
    ```bash
    python -m pip install paddlepaddle==2.6.0 -i https://mirror.baidu.com/pypi/simple
    ```

3. **Download the PaddleOCR Package**
    Navigate to your Python 3.8 site-packages folder in the conda environment folder and clone the PaddleOCR repository:
    
    ```bash
    cd anaconda3/envs/paddleocr/lib/python3.8/site-packages
    git clone https://github.com/PaddlePaddle/PaddleOCR
    cd PaddleOCR
    pip3 install -r requirements.txt
    ```

4. **Prepare the Dataset**
    Ensure that the dataset is in the correct format for PaddleOCR. Each image should have a corresponding label file with bounding box coordinates and text labels.

5. **Download Pre-trained Weights**
    Download the required pre-trained weights from the PaddleOCR GitHub repository and set it up for fine-tuning.

6. **Configure the YAML File**
    Configure your YAML file with the required training parameters.

7. **Fine-Tune the Model**
    Use the following command to train the PaddleOCR model on the generated dataset:
    ```bash
    paddleocr --train --dataset_dir ./dataset --output_dir ./output
    ```

8. **Export to Inference Model**
    Export the trained model to an inference model.

9. **Create the Second Conda Environment**
    Create the second conda environment with Python 3.8 for the PaddleOCR API:
    ```bash
    conda create --name paddleocr_infer python=3.8
    ```

10. **Install PaddleOCR in the Second Environment**
     Install PaddleOCR:
     ```bash
     conda activate paddleocr_infer
     pip install paddleocr
     ```

11. **Write an Inference Script**
     Write an inference script to test out your fine-tuned model.

### Detailed Steps

#### Install PaddleOCR
First, install PaddleOCR:
```bash
pip install paddleocr
```

#### Train the Model
Use the following command to train the PaddleOCR model on the generated dataset:
```bash
paddleocr --train --dataset_dir ./dataset --output_dir ./output
```

#### Evaluate the Model
Use the following command to evaluate the trained model:
```bash
paddleocr --eval --dataset_dir ./dataset --model_dir ./output
```

## Requirements
- Python 3.x
- Required libraries: `opencv-python-headless`, `Pillow`, `albumentations`, `paddleocr`

Install the required libraries using:
```bash
pip install opencv-python-headless pillow albumentations paddleocr
