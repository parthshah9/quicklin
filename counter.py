import os.path
from glob import glob


folders = glob('/home/linshaonju/BlensorResult_test/*/')

counter = 0

for f in folders:
	if os.path.exists(os.path.join(f, 'MulticutResults')):
		counter = counter + 1

print(counter)