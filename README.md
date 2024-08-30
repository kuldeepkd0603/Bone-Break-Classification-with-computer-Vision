"# Bone-Break-Classification-with-computer-Vision" 
# Bone Break Classification Project

## Overview

This project involves a deep learning model designed to classify bone fractures based on input images. The application provides a web interface where users can upload images of bone fractures, and the model predicts the type of fracture. Additionally, it displays detailed information about the predicted fracture type, including an overview, symptoms, causes, diagnosis, treatment, and prognosis.

## Features

- **Image Classification**: Predicts the type of bone fracture from an input image.
- **Detailed Information**: Provides comprehensive information about each type of fracture.
- **Web Interface**: User-friendly interface to upload images and view results.

## Project Structure

- `app.py`: The main Flask application file that handles image uploading, prediction, and rendering results.
- `bone_break_classify.h5`: The pre-trained Keras model for bone fracture classification.
- `templates/`
  - `index.html`: The home page for uploading images.
  - `result.html`: The result page displaying classification details and input image.
- `static/`
   -`uploads`
- `bone-break-classification-with-computer-vision.ipynb`: model building notbook .

Create a requirements.txt file with the following content:

<img src="static\image.png" alt="Alt Text" width="800"/>
<img src="static\image-1.png" alt="Alt Text" width="800"/>
<img src="static\image-2.png" alt="Alt Text" width="800"/>
<img src="static\image-3.png" alt="Alt Text" width="800"/>



## Model Architecture
- **Conv2D(60, (3, 3), activation='relu', input_shape=(256, 256, 3))**
- **MaxPooling2D((2, 2))**
- **Conv2D(120, (3, 3), activation='relu')**
- **MaxPooling2D((2, 2))**
- **Flatten()**
- **Dense(40, activation='relu')**
- **Dense(10, activation='softmax')**
## Model Architecture Summary
- **Input Layer**: Accepts 256x256 RGB images.
- **Convolutional Layers**: Three layers with increasing filter sizes (32, 64, 128) to extract features from the images.
- **Pooling Layers:**MaxPooling layers follow each convolutional layer to downsample the feature maps.
- **Flatten Layer:** Converts the 2D matrix of features into a vector for the fully connected layers.
- **Fully Connected Layers:** Two dense layers for learning non-linear combinations of the features; the last layer uses a sigmoid activation function for binary classification.
- **Dropout Layers:** Added to prevent overfitting by randomly dropping neurons during training
## Classes
The model classifies fractures into the following types:

- **Avulsion Fracture**
- **Comminuted Fracture**
- **Fracture Dislocation**
- **Greenstick Fracture**
- **Hairline Fracture**
- **Impaired Fracture**
- **Longitudinal Fracture**
- **Oblique Fracture**
- **Pathological Fracture**
- **Spiral Fracture**
