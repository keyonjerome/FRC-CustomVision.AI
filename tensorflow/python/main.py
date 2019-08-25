import sys
import numpy as np
from PIL import Image, ImageDraw
from object_detection import ObjectDetection
import cv2
import prediction_handling

MODEL_FILENAME = '../model.pb'
LABELS_FILENAME = '../labels.txt'

focal_length = 327.745
font = cv2.FONT_HERSHEY_SIMPLEX

def getDistanceToCamera(knownHeight, knownFocal, heightPixels):
    distance = -1
    if heightPixels > 0:
        distance = (knownHeight*knownFocal)/heightPixels
    return distance

def resize_down_to_1600_max_dim(image):
    h, w = image.shape[:2]
    if (h < 1600 and w < 1600):
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    return cv2.resize(image, new_size, interpolation = cv2.INTER_LINEAR)

def main():
    probability_threshold = 0.5
    
    cap = cv2.VideoCapture(2)
    
    _ , first_frame = cap.read()
    
    frame_shape = first_frame.shape

    prediction_handling.load()
    while True:
        ret, frame = cap.read()
        frame = resize_down_to_1600_max_dim(frame)
        predictions = prediction_handling.predict(frame)
        print(predictions)
        bestIndex = 0
        for x in range(len(predictions)):
            if predictions[x]['probability'] > predictions[bestIndex]['probability']:
                bestIndex = x
        if len(predictions) > 0:
            if predictions[bestIndex]['probability'] > probability_threshold:
                bBox = predictions[bestIndex]['boundingBox']
                print(bestIndex)
                left = int(bBox['left']*frame_shape[1])
                top = int(bBox['top']*frame_shape[0])
                width = int(bBox['width']*frame_shape[1])
                height = int(bBox['height']*frame_shape[0])
                print(left,top,width, height)
                print(frame_shape)
                cv2.rectangle(frame,(left,top),(left+width,top+height),(0,255,0),2)

                distToCamera = getDistanceToCamera(20,focal_length,height)
                distString = "Distance: " + str(distToCamera)
                cv2.putText(frame,distString,(frame_shape[0]-200,frame_shape[1]-200), font, 0.75,(255,255,255),2,cv2.LINE_AA)

        cv2.imshow('Image Processing',frame)
         # given an "x" input, end the program.
        givenKey = cv2.waitKey(500)
        # program end clause
        if givenKey == ord('x'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()


if __name__ == '__main__':
    main()


    