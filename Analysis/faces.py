from __future__ import print_function
import cv2, os
import numpy as np
from PIL import Image
from operator import itemgetter

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.createLBPHFaceRecognizer()
imageList = []
labelList = []
valueList = []
globalMeanValueList = []
globalValueList = []
panNumber = '34535434553'

def trainNew():
	for person in os.listdir("CroppedYale"):
		j = 0
		recognizer = cv2.face.createLBPHFaceRecognizer()
		for faceImageFile in os.listdir("CroppedYale/" + person + "/"):
			if faceImageFile.endswith(".pgm") or faceImageFile.endswith(".png"):
				if j % 2 == 0:	
					print ("File: " + faceImageFile)		
					faceImage = cv2.imread("CroppedYale/" + person + "/" + faceImageFile, 0)
				    	imageList.append(faceImage)
				    	labelList.append(hash(panNumber))
				j += 1
		recognizer.train(imageList, np.array(labelList))
		recognizer.save("CroppedYale/" + person + "/recognizer.yml")
		recognizer = None
		del imageList[:]
		del labelList[:]

def recognizeControl():
	setStat = []
	globalMean = 0
	globalImages = 0
	globalSumm = 0
	for person in os.listdir("CroppedYale"):
		f = open(person + "_con", "w")
		print("u s" , file=f)
		j = 0
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load("CroppedYale/" + person + "/recognizer.yml")
		mean = 0
		images = 0
		summ = 0
		for faceImageFile in os.listdir("CroppedYale/" + person):
			if faceImageFile.endswith(".pgm") or faceImageFile.endswith(".png"):
				if j % 2 == 0:
					faceImage = cv2.imread("CroppedYale/" + person + "/" + faceImageFile, 0)
				    	idd, distance = recognizer.predict(faceImage)
					images += 1
					globalImages += 1
					globalSumm += distance
					summ += distance
					valueList.append(distance)
					globalValueList.append(distance)					
				    	print (faceImageFile + " " + str(distance))
					print(str(images) + " " +  str(distance) , file=f)
				j += 1
			
		recognizer = None
		
		print ("Prosjeca udaljenost: " + str(float(summ/images)))
		print ("Maksimum: " + str(max(valueList)))
		print ("Minimum: " + str(min(valueList)))

		globalMeanValueList.append(float(summ/images))

		manjih = 0
		vecih = 0

		for value in valueList:
			if value < 37.6740299879:
				manjih += 1
			else:
				vecih += 1

		print ("Broj uzoraka manjih od prosjeka pozitivnih (38.2916230658): " +  str(manjih))
		print ("Broj uzoraka vecih+ od prosjeka pozitivnih (38.2916230658): " + str(vecih))

		setStat.append([person,float(summ/images),max(valueList),min(valueList),manjih,vecih])

		del valueList[:]

	print ("Globalna prosjeca udaljenost: " + str(float(globalSumm/globalImages)))
	print ("Globalni maksimum: " + str(max(globalValueList)))
	print ("Globalni minimum: " + str(min(globalValueList)))
	

	manjih = 0
	vecih = 0

	for value in globalMeanValueList:
		if value < 37.6740299879:
			manjih += 1
		else:
			vecih += 1
	
	print ("Ukupan broj slika: " + str(globalImages))
	print ("Broj prosjeka manjih od prosjeka pozitivnih (38.2916230658): " + str(manjih))
	print ("Broj prosjeka vevih od prosjeka pozitivnih (38.2916230658): " + str(vecih))

	for a,b,c,d,e,f in sorted(setStat, key=itemgetter(0)):
		print ("\\textbf{" + a + "} & " + str(b) + " & " + str(c) + " & " + str(d) + " & " + str(e) + " & " + str(f) + "\\\ \hline")

	del globalValueList [:]
	del globalMeanValueList [:]
			
	return

def recognizePositive():
	setStat = []
	globalMean = 0
	globalImages = 0
	globalSumm = 0
	for person in os.listdir("CroppedYale"):
		f = open(person + "_pos", "w")
		print("u s" , file=f)
		j = 0
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load("CroppedYale/" + person + "/recognizer.yml")
		mean = 0
		images = 0
		summ = 0
		for faceImageFile in os.listdir("CroppedYale/" + person):
			if faceImageFile.endswith(".pgm") or faceImageFile.endswith(".png"):
				if j % 2 != 0:
					faceImage = cv2.imread("CroppedYale/" + person + "/" + faceImageFile, 0)
				    	idd, distance = recognizer.predict(faceImage)
					images += 1
					globalImages += 1
					globalSumm += distance
					summ += distance
					valueList.append(distance)
					globalValueList.append(distance)					
					print(str(images * 60) + " " +  str(distance) , file=f)
				j += 1
			
		recognizer = None
		
		print ("Prosjeca udaljenost: " + str(float(summ/images)))
		print ("Maksimum: " + str(max(valueList)))
		print ("Minimum: " + str(min(valueList)))

		globalMeanValueList.append(float(summ/images))

		manjih = 0
		vecih = 0

		for value in valueList:
			if value < 37.6740299879:
				manjih += 1
			else:
				vecih += 1

		print ("Broj uzoraka manjih od prosjeka pozitivnih (38.2916230658): " +  str(manjih))
		print ("Broj uzoraka vecih+ od prosjeka pozitivnih (38.2916230658): " + str(vecih))

		setStat.append([person,float(summ/images),max(valueList),min(valueList),manjih,vecih])

		del valueList[:]

	print ("Globalna prosjeca udaljenost: " + str(float(globalSumm/globalImages)))
	print ("Globalni maksimum: " + str(max(globalValueList)))
	print ("Globalni minimum: " + str(min(globalValueList)))
	

	manjih = 0
	vecih = 0

	for value in globalMeanValueList:
		if value < 37.6740299879:
			manjih += 1
		else:
			vecih += 1
	
	print ("Ukupan broj slika: " + str(globalImages))
	print ("Broj prosjeka manjih od prosjeka pozitivnih (38.2916230658): " + str(manjih))
	print ("Broj prosjeka vevih od prosjeka pozitivnih (38.2916230658): " + str(vecih))

	for a,b,c,d,e,f in sorted(setStat, key=itemgetter(0)):
		print ("\\textbf{" + a + "} & " + str(b) + " & " + str(c) + " & " + str(d) + " & " + str(e) + " & " + str(f) + "\\\ \hline")

	del globalValueList [:]
	del globalMeanValueList [:]
			
	return

def recognizeNegative():
	setStat = []
	globalMean = 0
	globalImages = 0
	globalSumm = 0
	for originalPerson in os.listdir("CroppedYale"):
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load("CroppedYale/" + originalPerson + "/recognizer.yml")
		f = open(originalPerson + "_neg", "w")
		print("u s" , file=f)
		mean = 0
		images = 0
		summ = 0
		for person in os.listdir("CroppedYale"):
			if person != originalPerson:
				for faceImageFile in os.listdir("CroppedYale/" + person):
					if faceImageFile.endswith(".pgm") or faceImageFile.endswith(".png"):
						faceImage = cv2.imread("CroppedYale/" + person + "/" + faceImageFile, 0)
					    	idd, distance = recognizer.predict(faceImage)
						images += 1
						globalImages += 1
						globalSumm += distance
						summ += distance
						valueList.append(distance)
						globalValueList.append(distance)					
						print(str(images) + " " +  str(distance) , file=f)
			
		recognizer = None
		
		print ("Prosjeca udaljenost: " + str(float(summ/images)))
		print ("Maksimum: " + str(max(valueList)))
		print ("Minimum: " + str(min(valueList)))

		globalMeanValueList.append(float(summ/images))

		manjih = 0
		vecih = 0

		for value in valueList:
			if value < 37.6740299879:
				manjih += 1
			else:
				vecih += 1

		print ("Broj uzoraka manjih od prosjeka pozitivnih (38.2916230658): " +  str(manjih))
		print ("Broj uzoraka vecih+ od prosjeka pozitivnih (38.2916230658): " + str(vecih))

		setStat.append([person,float(summ/images),max(valueList),min(valueList),manjih,vecih])

		del valueList[:]

	print ("Globalna prosjeca udaljenost: " + str(float(globalSumm/globalImages)))
	print ("Globalni maksimum: " + str(max(globalValueList)))
	print ("Globalni minimum: " + str(min(globalValueList)))
	

	manjih = 0
	vecih = 0

	for value in globalMeanValueList:
		if value < 37.6740299879:
			manjih += 1
		else:
			vecih += 1
	
	print ("Ukupan broj slika: " + str(globalImages))
	print ("Broj prosjeka manjih od prosjeka pozitivnih (38.2916230658): " + str(manjih))
	print ("Broj prosjeka vevih od prosjeka pozitivnih (38.2916230658): " + str(vecih))

	for a,b,c,d,e,f in sorted(setStat, key=itemgetter(0)):
		print ("\\textbf{" + a + "} & " + str(b) + " & " + str(c) + " & " + str(d) + " & " + str(e) + " & " + str(f) + "\\\ \hline")

	del globalValueList [:]
	del globalMeanValueList [:]
			
	return

def extractFaces():
	i = 0
	for faceImageFile in os.listdir("."):
		if faceImageFile.endswith(".jpg"):
			print (faceImageFile)
			i += 1
			faceImage = cv2.imread(faceImageFile, 0)
			faces = faceCascade.detectMultiScale(faceImage)
			for (x, y, w, h) in faces:
				cv2.imwrite(str(i)+".png", faceImage[y: y + h, x: x + w])

trainNew()
recognizeControl()
recognizePositive()
recognizeNegative()
#recognize()
