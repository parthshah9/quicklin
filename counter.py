import os.path
from glob import glob


folders = glob('/home/linshaonju/BlensorResult_test/*/')

counter = 0

for f in folders:
	if os.path.exists(os.path.join(f, 'MulticutResults')):
		counter = counter + 1

	pngs = glob(os.path.join(f, '*.ppm'))
	if (not len(pngs) == 2):
		print(f)

print(counter)
