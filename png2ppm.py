#!/usr/bin/env python
from glob import glob                                                           
import cv2 
pngs = glob('/home/linshaonju/BlensorResult_test/*/*.png')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'ppm', img)
