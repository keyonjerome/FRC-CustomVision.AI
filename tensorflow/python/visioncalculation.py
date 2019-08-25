
def find_best_probability_index(predictions): 
    bestIndex = 0 
    for x in range(len(predictions)):   
        if predictions[x]['probability'] > predictions[bestIndex]['probability']:
            bestIndex = x
    return bestIndex

def find_object_corners(predictions,bestIndex,probability_threshold,frame_shape):
        
        if len(predictions) > 0:
           
            if predictions[bestIndex]['probability'] > probability_threshold:
                print(predictions[bestIndex])
                # get the bounding box of the object
                bBox = predictions[bestIndex]['boundingBox']
                
                # convert the decimal position of the left side of the bounding box to an x-coordinate
                left = int(bBox['left']*frame_shape[1])
                # convert the decimal position of the top side of the bounding box to an y-coordinate
                top = int(bBox['top']*frame_shape[0])
                # convert the decimal width of the bounding box to pixels
                width = int(bBox['width']*frame_shape[1])
                # convert the decimal height of the bounding box to pixels 
                height = int(bBox['height']*frame_shape[0])
 
                top_left_corner = (left,top)
                bottom_right_corner = (left+width,top+height)

                return top_left_corner, bottom_right_corner,width, height

        return (0,0), (0,0),0,0                  

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
