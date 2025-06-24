import os
import cv2
from ultralytics import YOLOv10
import psutil
import torch

config_path = './config.yaml'

# Load a model
model = YOLOv10.from_pretrained("jameslahm/yolov10n")  # load pre trained model

# Use the model
model.train(data=config_path, epochs=200, batch=32)  # Train the model




