import sys
import cntk
import numpy as np
from PIL import Image, ImageDraw
from object_detection import ObjectDetection
from cntk_predict import CNTKObjectDetection
import cv2

MODEL_FILENAME = 'model.onnx'
LABELS_FILENAME = 'labels.txt'
focal_length = 327.745
font = cv2.FONT_HERSHEY_SIMPLEX

def getDistanceToCamera(knownHeight, knownFocal, heightPixels):
    distance = -1
    if heightPixels > 0:
        distance = (knownHeight*knownFocal)/heightPixels
    return distance

def main():
    probability_threshold = 0
    cap = cv2.VideoCapture(0)
    model = cntk.Function.load(MODEL_FILENAME, format=cntk.ModelFormat.ONNX)
    _, first_frame = cap.read()
    frame_shape = first_frame.shape
    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    od_model = CNTKObjectDetection(model, labels)
    while True:
        ret, frame = cap.read()
        #frame = cv2.imread("testimage.jpg")
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        predictions = od_model.predict_image(pil_frame)

        bestIndex = 0
        for x in range(len(predictions)):
            if predictions[x]['probability'] > predictions[bestIndex]['probability']:
                bestIndex = x
        if len(predictions) > 0:
            if predictions[bestIndex]['probability'] > probability_threshold:
                bBox = predictions[bestIndex]['boundingBox']
                
                x = int(bBox['left']*frame_shape[0])
                y = int(bBox['top']*frame_shape[1])
                w = int(bBox['width']*frame_shape[0])
                h = int(bBox['height']*frame_shape[1])

                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                distToCamera = getDistanceToCamera(20,focal_length,h)
                distString = "Distance: " + str(distToCamera)
                cv2.putText(frame,distString,(frame_shape[0]-200,frame_shape[1]-200), font, 0.75,(255,255,255),2,cv2.LINE_AA)

        cv2.imshow('Image Processing',frame)
         # given an "x" input, end the program.
        givenKey = cv2.waitKey(1)
        # program end clause
        if givenKey == ord('x'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()


if __name__ == '__main__':
    main()


    