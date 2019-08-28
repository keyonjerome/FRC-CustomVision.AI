import sys
import numpy as np
from PIL import Image, ImageDraw
from object_detection import ObjectDetection
import visioncalculation
import cv2
import prediction_handling
import networking

#focal_length = 327.745
focal_length = 708.897
font = cv2.FONT_HERSHEY_SIMPLEX
probability_threshold = 0.75

def main():
    # open a video capture
    cap = cv2.VideoCapture(2)
    # read the first frame from the camera
    _ , first_frame = cap.read()
    # get shape (resolution) of camera from first frame
    frame_shape = first_frame.shape

    # load the tensorflow model, setup
    prediction_handling.load()

    networking.initialize()
    #networking.wait_for_connection()

    while True:
        # read frame from camera
        ret, frame = cap.read()
        # resize frame
        frame = visioncalculation.resize_down_to_1600_max_dim(frame)
        # feed frame into model
        predictions = prediction_handling.predict(frame)
        
        # find best 
        bestIndex = visioncalculation.find_best_probability_index(predictions)
        
        # find top left & bottom right corner of object, object width and height
        top_left, bottom_right,width, height = visioncalculation.find_object_corners(predictions,bestIndex,probability_threshold,frame_shape)
        # calculate distance from object to camera
        distance_to_camera = visioncalculation.getDistanceToCamera(11,focal_length,height)
        # draw object outline and distance data to screen, show it
        show_frame(frame,top_left,bottom_right,distance_to_camera,frame_shape)
        
         # given an "x" input, end the program.
        givenKey = cv2.waitKey(500)
        # program end clause
        if givenKey == ord('x'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

# Draw object outline and vision data to screen, then show it
def show_frame(frame,obj_top_left,obj_bottom_right,distance,frame_shape):

    cv2.rectangle(frame,obj_top_left,obj_bottom_right,(0,255,0),2)

    distance_string = "Distance: " + str(distance)

    cv2.putText(frame,distance_string,(frame_shape[0]-200,frame_shape[1]-200), font, 0.75,(255,255,255),2,cv2.LINE_AA)

    cv2.imshow('Image Processing',frame)

if __name__ == '__main__':
    main()


    