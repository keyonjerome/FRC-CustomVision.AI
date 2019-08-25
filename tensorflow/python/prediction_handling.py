# Suggested steps before inference: 
# 1. for an image of width and height being (w, h) pixels, resize image to (w', h'), where w/h = w'/h' and w' x h' = 262144
# 2. resize network input size to (w', h')
# 3. pass the image to network and do inference
# (4. if inference speed is too slow for you, try to make w' x h' smaller)
import sys
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
from object_detection import ObjectDetection

MODEL_FILENAME = '../model.pb'
LABELS_FILENAME = '../labels.txt'
od_model = 0

class TFObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow
    """
    def __init__(self, graph_def, labels):
        super(TFObjectDetection, self).__init__(labels)
        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
            
    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float)[:,:,(2,1,0)] # RGB -> BGR

        with tf.Session(graph=self.graph) as sess:
            output_tensor = sess.graph.get_tensor_by_name('model_outputs:0')
            outputs = sess.run(output_tensor, {'Placeholder:0': inputs[np.newaxis,...]})
            return outputs[0]


def load():
    global od_model
    # Load a TensorFlow model
    graph_def = tf.GraphDef()
    with tf.gfile.FastGFile(MODEL_FILENAME, 'rb') as f:
        graph_def.ParseFromString(f.read())

    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    od_model = TFObjectDetection(graph_def, labels)

def predict(frame):
    pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    predictions = od_model.predict_image(pil_frame)
    return predictions
