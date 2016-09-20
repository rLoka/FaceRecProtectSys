unilist = []
for i in xrange(256):
	string = str(bin(i))
	string = string.replace('0b','')

	while len(string) < 8:
		string = '0' + string

	lastbit = 0
	changes = 0

	for k in xrange (len(string)):
		if k == 0:
			lastbit = string[k]
		else:
			if lastbit != string[k]:
				changes += 1
		lastbit = string[k]
	
	if changes <= 2:
		print string
		unilist.append(string)

print 'Ukupno UNI: ', len(unilist)
		
