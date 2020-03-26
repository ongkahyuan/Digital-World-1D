import numpy as np
import time
import cv2
import os
import threading

class yolo_manager(threading.Thread):
    """Checks if the room is occupied when called"""

    def __init__(self, interval=10):
        # load the COCO class labels our YOLO model was trained on
        if __name__ == "__main__":
            labelsPath = "Yolo_reqs/coco.names"
            weightsPath = "Yolo_reqs/yolov3.weights"
            configPath = "Yolo_reqs/yolov3.cfg"
        else:
            labelsPath = "YOLO/Yolo_reqs/coco.names"
            weightsPath = "YOLO/Yolo_reqs/yolov3.weights"
            configPath = "YOLO/Yolo_reqs/yolov3.cfg"
        self.LABELS = open(labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
            dtype="uint8")



        # load yolo trained on COCO dataset
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        
        threading.Thread.__init__(self)
        self.room_state = None
        self.stop = False
        self.interval = interval

    def check_room_state(self):
        # print("am checking")
        # set video capture device as the webcam
        self.cap = cv2.VideoCapture(0)
        ret, image = self.cap.read()
        self.cap.release()
        (H, W) = image.shape[:2]
        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(ln)

        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > 0.5:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

        objects_in_scene = []
        number_of_objects = {"person":0, "laptop":0, "backpack":0}

        for i in idxs.flatten():
            try:
                objects_in_scene.append(self.LABELS[classIDs[i]])
            except:
                pass

        for i in objects_in_scene:
            if i == "person":
                number_of_objects['person'] += 1
            if i == "laptop":
                number_of_objects['laptop'] += 1
            if i == "bag":
                number_of_objects['backpack'] += 1
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)
        return number_of_objects
    
    def stop_all(self):
        self.stop = True
        
    
    def run(self):
        while self.stop != True:
            self.room_state = self.check_room_state()
            time.sleep(self.interval)

if __name__ == "__main__":
    
    yolo_obj = yolo_manager()
    yolo_obj.check_room_state()

