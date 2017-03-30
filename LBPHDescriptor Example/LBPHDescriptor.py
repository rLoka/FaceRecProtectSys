from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np

img_filename = "image.jpg"
im = Image.open(img_filename).convert('LA')
nim = Image.new('LA', im.size)
pixels = nim.load()

bitlist = []
pixelvalueslist = []
pixelplot = []
radius = 5

for i in xrange(5, im.size[0]-5):    # for every pixel:
    for j in xrange(5, im.size[1]-5):

	if im.getpixel((i,j)) >= im.getpixel((i-radius,j-radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i,j-radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i+radius,j-radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i-radius,j)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i+radius,j)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i-radius,j+radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i,j+radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')

	if im.getpixel((i,j)) >= im.getpixel((i+radius,j+radius)):
		bitlist.append('0')
	else:
		bitlist.append('1')
	
	lastbit = 0
	changes = 0

	for k in xrange (len(bitlist)):
		if k == 0:
			lastbit = bitlist[k]
		else:
			if lastbit != bitlist[k]:
				changes += 1
		lastbit = bitlist[k]

	print 'BITLIST:' + ''.join(bitlist)
	print 'CHANGES:', changes
	print 'VALUE:', int(''.join(bitlist), 2)

	if changes > 1:
		pixels[i,j] = 0
		pixelvalueslist.append(0)
		pixelplot.append([i, j, 0])  
	else:
		pixels[i,j] = int(''.join(bitlist), 2)	
		pixelvalueslist.append(int(''.join(bitlist), 2))
		pixelplot.append([i, j, int(''.join(bitlist), 2)])     

	del bitlist[:]	

nim.show()
xbins = range(0, 255)
print 'XBINS:', xbins
plt.hist(pixelvalueslist, bins=xbins, color='blue')
plt.show()

