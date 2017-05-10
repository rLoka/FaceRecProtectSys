from __future__ import print_function
import cv2, os
import numpy as np
from PIL import Image
from operator import itemgetter

recognizer = cv2.face.createLBPHFaceRecognizer()
imageList = []
labelList = []

for person in os.listdir("Users"):
	j = 0
	recognizer = cv2.face.createLBPHFaceRecognizer()
	for faceImageFile in os.listdir("Users/" + person + "/"):
		if faceImageFile.endswith(".png"):
			print ("File: " + faceImageFile)		
			faceImage = cv2.imread("Users/" + person + "/" + faceImageFile, 0)
		    	imageList.append(faceImage)
		    	labelList.append(hash(person))
	recognizer.train(imageList, np.array(labelList))
	recognizer.save("Users/" + person + "/" + person + ".yml")
	recognizer = None
	del imageList[:]
	del labelList[:]


