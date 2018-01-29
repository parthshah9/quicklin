import os.path
from glob import glob


f = open('commands.txt','w')
f.write('python png2ppm.py')

folders = glob('/home/linshaonju/BlensorResult_test/*/')

for j in pngs:
	f.write('./motionseg_release ' + os.path.join(j, 'test.bmf') + ' 0 2 4 0.5' )

# images = []
#     for flow_map in glob.iglob(os.path.join(dir,'*_flow.flo')):
#         flow_map = os.path.basename(flow_map)
#         root_filename = flow_map[:-9]
#         img1 = root_filename+'_img1.ppm'
#         img2 = root_filename+'_img2.ppm'
#         if not (os.path.isfile(os.path.join(dir,img1)) or os.path.isfile(os.path.join(dir,img2))):
#             continue

f.close() 