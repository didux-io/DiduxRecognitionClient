'''
Haar Cascade Face detection with OpenCV
    Based on tutorial by pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
Adapted by Marcelo Rovai - MJRoBot.org @ 7Feb2018
'''
import numpy as np
import argparse
import time
import cv2

# construct the argument parse and parse the arguments
from utils.fps import FPS
from utils.stream import WebcamVideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default="models/deploy.prototxt.txt", help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", default="models/res10_300x300_ssd_iter_140000.caffemodel", help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
ap.add_argument("-n", "--num-frames", type=int, default=120, help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
args = vars(ap.parse_args())

# load our serialized model from disk
print("[INFO] loading model...")
face_cascade = cv2.CascadeClassifier('models/lbpcascade_frontalface_improved.xml')
# net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = WebcamVideoStream(src=0).start()
vs.resolution = (640, 480)
time.sleep(2.0)

cv2.namedWindow("Didux.io", cv2.WINDOW_NORMAL)
fps = FPS().start()

# loop over the frames from the video stream
while True:

    frame = vs.read()

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    #
    # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
    #                              (300, 300), (104.0, 177.0, 123.0))
    #
    # # pass the blob through the network and obtain the detections and
    # # predictions
    # net.setInput(blob)
    # detections = net.forward()

    # # loop over the detections
    # for i in range(0, detections.shape[2]):
    #     # extract the confidence (i.e., probability) associated with the
    #     # prediction
    #     confidence = detections[0, 0, i, 2]
    #     # filter out weak detections by ensuring the `confidence` is
    #     # greater than the minimum confidence
    #     if confidence < args["confidence"]:
    #         continue
    #     # compute the (x, y)-coordinates of the bounding box for the
    #     # object
    #     box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    #     (startX, startY, endX, endY) = box.astype("int")
    #
    #     # draw the bounding box of the face along with the associated
    #     # probability
    #     text = "{:.2f}%".format(confidence * 100)
    #     y = startY - 10 if startY - 10 > 10 else startY + 10
    #     cv2.rectangle(frame, (startX, startY), (endX, endY),
    #                   (0, 0, 255), 2)
    #     cv2.putText(frame, text, (startX, y),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # show the output frame
    cv2.imshow("Didux.io", frame)
    cv2.setWindowProperty('Didux.io', cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty('Didux.io', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    fps.update()
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    if fps._numFrames < args["num_frames"]:
        fps.update()
    if fps._numFrames == args["num_frames"]:
        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        fps.start()

cv2.destroyAllWindows()
cv2.waitKey(1)
vs.stop()
