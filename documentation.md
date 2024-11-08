# Dcoumentation

## Synthetic Dataset
I have used two datasets. One is generated through PIL-based script which generates A4 pages. Another is my modified version of TRDR script which generates and augments text datasets.
The synthetic dataset is generated using the `textgencv2.py` script. This script overlays random text snippets on scanned paper textures or plain backgrounds and applies various transformations to simulate real-world document conditions.

### Transformations Applied

- **Rotation**: Randomly rotates the text to simulate different orientations.
- **Skewing**: Applies skew transformations to mimic scanned documents.
- **Noise**: Adds random noise to simulate poor scan quality.
- **Lighting Adjustments**: Changes brightness and contrast to simulate different lighting conditions.
- **Text Fonts/Styles**: Uses different fonts and styles to simulate various document types.
- **Shadow**: Adds shadows to simulate lighting effects.
- **Ink Bleed**: Simulates ink bleed to mimic printed documents.
- **Fold Lines**: Adds fold lines to simulate folded documents.

## TRDG Dataset

The Text Recognition Data Generator (TRDG) is used to generate additional datasets with specific configurations. The following commands are used to generate 1500 images:

```bash
# Example command to generate images
trdg -c 1500 -w 5 -f 64
```

# Model Training
Note: I haven't attached the model in this notebook! So for fine tuning, model needs to be added separately to this notebook!

The model training process involves using the generated synthetic dataset to train a text detection model. The model used in this project is a custom text detection model PaddleOCR designed for this task.

## Training Process

1. Load the synthetic dataset.
2. Preprocess the images and annotations.
3. Train the custom text detection model on the dataset.
4. Save the trained model for evaluation.

# Evaluation

The trained model is evaluated on a separate test set to measure its performance. The following metrics are used:

- **Accuracy**: Measures the overall correctness of the model.
- **Precision**: Measures the proportion of true positive detections among all positive detections.
- **Recall**: Measures the proportion of true positive detections among all actual positives.
- **IoU (Intersection over Union)**: Measures the overlap between the predicted bounding boxes and the ground truth.

# Corner Cases Considered

## During Dataset Generation

- **Curved Text**: Generates text snippets with curved paths to simulate handwritten or artistic text.
- **Text Overlapping**: Simulates overlapping text to test the model's ability to detect individual text snippets.
- **Different Fonts and Sizes**: Uses a variety of fonts and sizes to ensure the model can handle diverse text styles.
- **Background Variations**: Uses different background textures and colors to simulate various document types.
- **Text Occlusions**: Adds occlusions to test the model's robustness in detecting partially covered text.

## Overall

- **Realistic Document Scenarios**: Simulates real-world document conditions such as folds, shadows, and ink bleed.
- **Random Transformations**: Applies random transformations to ensure the model can handle diverse and unpredictable conditions.