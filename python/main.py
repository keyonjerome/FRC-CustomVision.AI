import sys
import cntk
import numpy as np
from PIL import Image, ImageDraw
from object_detection import ObjectDetection
from cntk_predict import CNTKObjectDetection

MODEL_FILENAME = 'model.onnx'
LABELS_FILENAME = 'labels.txt'

def main():
    model = cntk.Function.load(MODEL_FILENAME, format=cntk.ModelFormat.ONNX)
    
    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    od_model = CNTKObjectDetection(model, labels)

    image = Image.open("testimage.jpg")
    predictions = od_model.predict_image(image)
    print(predictions)


if __name__ == '__main__':
    main()


    