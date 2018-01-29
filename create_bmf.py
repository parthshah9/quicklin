#!/usr/bin/env python
from glob import glob                                                           
import os.path

folders = glob('/home/linshaonju/BlensorResult_test/*/')


for j in folders:
	print j

	f = open(os.path.join(j,'test.bmf'),'w')
	f.write('2 1\n')

	ppms = glob(os.path.join(j, '*.ppm'))

	for i in ppms:
		print(i)
		f.write(os.path.basename(i) + '\n')

	f.close()

    # img = cv2.imread(j)
    # cv2.imwrite(j[:-3] + 'ppm', img)
