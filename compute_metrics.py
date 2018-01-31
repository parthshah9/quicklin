import cv2
import numpy as np
from PIL import Image
from scipy.misc import imread
import scipy
import os.path
from glob import glob
### LOGGING ####

f = open('logging.txt', 'w')
f.write('folder_number  density  precision  recall  f-measure  extracted_objects  total_objects\n')

### INITIALIZATIONS ###

height = 240
width = 320

folder_counter = 0

TOTAL_DENSITY = 0
TOTAL_PRECISION = 0
TOTAL_RECALL = 0
TOTAL_F = 0
TOTAL_OBJECTS_EXTRACTED = 0
TOTAL_OBJECTS_SEEN = 0



### LOADING ####


# segments_in_img = Image.open('/afs/cs.stanford.edu/u/pshah9/Lin/final/4000/MulticutResults/ldof0.5000004/Segments001.ppm')
# colors = segments_in_img.convert('RGB').getcolors()
# print(colors)

valid_folders = glob('/home/linshaonju/BlensorResult_test/*/MulticutResults/ldof0.5000004/Segments001.ppm')


for folder in valid_folders:

	label_location = os.path.join(os.sep.join(p.split(os.sep)[:-3]), 'frame80_labeling.npz')


	loaded = np.load(label_location)
	gt = loaded['labeling']


	segments_in_scipy = imread(folder)

	folder_number = os.sep.join(p.split(os.sep)[4:-3])
	f.write(folder_number + '  ')


	### PREPROCESSING ###

	#REMOVE ANY GRAY
	for i in range(height):
		for j in range(width):
			if np.all(segments_in_scipy[i][j] == (230,230,230)):
				segments_in_scipy[i][j] = (255, 255, 255)



	### CREATE DICTIONARIES ####

	dict_seg = {}
	seg_all_locations = []

	#CREATE DICTIONARY OF COLORS AND LOCATIONS
	for i in range(height):
		for j in range(width):
			if not np.all(segments_in_scipy[i][j] == (255, 255, 255)):
				if (segments_in_scipy[i][j][0], segments_in_scipy[i][j][1], segments_in_scipy[i][j][2]) in dict_seg:
					dict_seg[(segments_in_scipy[i][j][0], segments_in_scipy[i][j][1], segments_in_scipy[i][j][2])].append((i,j))
					seg_all_locations.append((i,j))
				else:
					dict_seg[(segments_in_scipy[i][j][0], segments_in_scipy[i][j][1], segments_in_scipy[i][j][2])] = [(i,j)]

	# print(dict_seg.keys())

	dict_labels = {}
	labels_all_locations = []

	#CREATE DICTIONARY OF COLORS AND LOCATIONS
	for i in range(height):
		for j in range(width):
			if not np.all(gt[i][j] == (0, 0, 0)):
				if (gt[i][j][0], gt[i][j][1], gt[i][j][2]) in dict_labels:
					dict_labels[(gt[i][j][0], gt[i][j][1], gt[i][j][2])].append((i,j))
					labels_all_locations.append((i,j))
				else:
					dict_labels[(gt[i][j][0], gt[i][j][1], gt[i][j][2])] = [(i,j)]

	# print(dict_labels.keys())





	### CALC METRICS ###

	# AVERAGE REGION DENSITY = defined as the average percentage coverage over all ground truth regions

	overlap = set(seg_all_locations) & set(labels_all_locations)


	# print('total pixels in segmentation = %d' % len(seg_all_locations))
	# print('total pixels in labels = %d' %len(labels_all_locations))
	# print('overlap = %d' % len(overlap))


	average_region_density = float(len(overlap)) / len(labels_all_locations)
	# print('Average region density = %f' % (average_region_density))

	f.write('%f  ' % average_region_density)
	TOTAL_DENSITY += average_region_density



	seg_keys = dict_seg.keys()
	labels_keys = dict_labels.keys()

	num_seg = len(seg_keys)
	num_labels = len(labels_keys)





	# PRECISION = Intersection of segmented and labeled over size of segmented
	precision_matrix = np.zeros((num_labels, num_seg))

	for i in range(num_labels):
		for j in range(num_seg):
			intersec = set(dict_labels[labels_keys[i]]) & set(dict_seg[seg_keys[j]])

			precision_matrix[i,j] = float(len(intersec)) / len(set(dict_seg[seg_keys[j]]))

	# print(precision_matrix)
	average_precision = np.sum(precision_matrix) / len(labels_keys)
	# print('Average precision = %f' % (average_precision))

	if num_labels > num_seg:
		precision_matrix = np.hstack((precision_matrix, np.ones((num_labels, num_labels - num_seg))))

	f.write('%f  ' % average_precision)
	TOTAL_PRECISION += average_precision



	#RECALL = Intersection of segmented and labeled over size of labeled
	recall_matrix = np.zeros((num_labels, num_seg))


	for i in range(num_labels):
		for j in range(num_seg):
			intersec = set(dict_labels[labels_keys[i]]) & set(dict_seg[seg_keys[j]])

			recall_matrix[i,j] = float(len(intersec)) / len(set(dict_labels[labels_keys[i]]))

	# print(recall_matrix)
	average_recall = np.sum(recall_matrix) / len(labels_keys)
	# print('Average recall = %f' % (average_recall))

	if num_labels > num_seg:
		recall_matrix = np.hstack((recall_matrix, np.zeros((num_labels, num_labels - num_seg))))

	f.write('%f  ' % average_recall)
	TOTAL_RECALL += average_recall



	#Fscore = elementwise(P,R)/(P + R)
	f_score_matrix = np.zeros((num_labels, num_labels))

	f_score_matrix = np.nan_to_num((np.divide(2*np.multiply(precision_matrix, recall_matrix), np.add(precision_matrix, recall_matrix))))

	# print(f_score_matrix)

	assignments = scipy.optimize.linear_sum_assignment(-1*f_score_matrix)

	# print(assignments)

	f_score_sum = 0

	for i in range(num_labels):
		f_score_sum += f_score_matrix[assignments[0][i], assignments[1][i]]

	f_score_average = f_score_sum / num_labels
	# print('Average f score = %f' % (f_score_average))

	f.write('%f  ' % f_score_average)
	TOTAL_F += f_score_average


	#Object recogntion = if f_score is above 75%
	recognized_objects = 0
	total_objects = num_labels

	for i in range(len(dict_labels.keys())):
		if f_score_matrix[assignments[0][i], assignments[1][i]] > 0.75:
			recognized_objects += 1

	# print('Number of recognized objects = %d. Number of total objects = %d' % (recognized_objects, total_objects))

	f.write('%d  %d\n' % (recognized_objects, total_objects))
	TOTAL_OBJECTS_EXTRACTED += recognized_objects
	TOTAL_OBJECTS_SEEN += total_objects

	print('[%s] running averages: density = %f | precision = %f | recall = %f | f_score = %f | objects extracted = %f | objects seen = %f '
		 % (folder_number, TOTAL_DENSITY / folder_counter, TOTAL_PRECISION / folder_counter, TOTAL_RECALL / folder_counter, TOTAL_F / folder_counter,
		 	TOTAL_OBJECTS_EXTRACTED, TOTAL_OBJECTS_SEEN))

	# Iterate over all possible files and then also output to the screen intermittently
	folder_counter += 1

f.write('TOTAL_DENSITY = %f\n' % TOTAL_DENSITY)
f.write('TOTAL_PRECISION = %f\n' % TOTAL_PRECISION)
f.write('TOTAL_RECALL = %f\n' % TOTAL_RECALL)
f.write('TOTAL_F = %f\n' % TOTAL_F)
f.write('TOTAL_OBJECTS_EXTRACTED = %f\n' % TOTAL_OBJECTS_EXTRACTED)
f.write('TOTAL_OBJECTS_SEEN = %f\n' % TOTAL_OBJECTS_SEEN)

f.write('\n')
f.write('\n')

f.write('FINAL VALUES\n')
f.write('total folders visited = %d' % folder_counter)
f.write('AVERAGE_DENSITY = %f\n' % TOTAL_DENSITY / folder_counter)
f.write('AVERAGE_PRECISION = %f\n' % TOTAL_PRECISION / folder_counter)
f.write('AVERAGE_RECALL = %f\n' % TOTAL_RECALL / folder_counter)
f.write('AVERAGE_F = %f\n' % TOTAL_F / folder_counter)
f.write('TOTAL_OBJECTS_EXTRACTED = %f\n' % TOTAL_OBJECTS_EXTRACTED)
f.write('TOTAL_OBJECTS_SEEN = %f\n' % TOTAL_OBJECTS_SEEN)

f.close()