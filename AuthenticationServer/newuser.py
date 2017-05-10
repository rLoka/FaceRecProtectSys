from __future__ import print_function
import cv2, os
import numpy as np
from imutils import face_utils
import argparse
import imutils
import dlib
import cv2
from sympy import Point, Line, mpmath
from mpmath import *
from operator import itemgetter
from PIL import Image

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("ldm.dat")
recognizer = cv2.face.createLBPHFaceRecognizer()
imageList = []
labelList = []


def calculateFaceTilt(leftEye, rightEye):
    zeroLine = Line(Point(1, 0), Point(0, 0))
    eyeMiddlePoint = Point((leftEye + rightEye) / 2)
    eyeLine = Line(leftEye, rightEye)
    angle = mpmath.degrees(eyeLine.angle_between(zeroLine))
    if (leftEye.y > rightEye.y):
        return int(angle) - 180
    else:
        return 180 - int(angle)


def rotateImage(imageObj, correctionAngle, nosePoint):
    rotationMatrix = cv2.getRotationMatrix2D(nosePoint, correctionAngle, 1.0)
    return cv2.warpAffine(imageObj, rotationMatrix, (imageObj.shape[1], imageObj.shape[0]), flags=cv2.INTER_LINEAR)


for person in os.listdir("Users"):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    for faceImageFile in os.listdir("Users/" + person + "/originals"):
        if faceImageFile.endswith(".png"):
            gray = cv2.imread("Users/" + person + "/originals/" + faceImageFile,
                          cv2.CV_8UC1)  # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)

            for (j, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                angle = calculateFaceTilt(Point(shape[39]), Point(shape[42]))

                gray = rotateImage(gray, angle, tuple(shape[33]))
                # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 1)

                # loop over the face detections
                for (k, rect) in enumerate(rects):
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    eye = Point(shape[37])
                    eyebrow = Point(shape[19])
                    left = Point(min(shape, key=itemgetter(0)))
                    top = Point(min(shape, key=itemgetter(1)))
                    right = Point(max(shape, key=itemgetter(0)))
                    bottom = Point(max(shape, key=itemgetter(1)))

                    gray = gray[int(top.y - eye.distance(eyebrow) / 2):int(top.y + top.distance(bottom)),
                           int(left.x):int(left.x + left.distance(right))]

                    # ujednacavanje histograma
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    gray = clahe.apply(gray)
                    # gray = cv2.bilateralFilter(gray, 9, 75, 75)

                    ratio = 300.0 / gray.shape[1]
                    dimensions = (300, int(gray.shape[0] * ratio))

                    gray = cv2.resize(gray, dimensions, interpolation=cv2.INTER_AREA)
                    cv2.imwrite("Users/" + person + "/processed/" + faceImageFile, gray)

                    print("File: " + faceImageFile)
                    # faceImage = cv2.imread("Users/" + person + "/" + faceImageFile, 0)
            imageList.append(gray)
            labelList.append(hash(person))
    recognizer.train(imageList, np.array(labelList))
    recognizer.save("Users/" + person + "/" + person + ".yml")
    recognizer = None
    del imageList[:]
    del labelList[:]
