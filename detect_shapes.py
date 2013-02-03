import numpy as np
import cv2
import Image, cv
import matplotlib.pyplot as plt
from smooth import smooth
import math
from color_classification import avg_img_color_np, min_distance_index
from colors import color_names

def x_var_filter(l):
	ans = np.std(l, 0)
	x, y = ans[0]
	if x * 1.9 > y:
		return False
	else:
		return True


f = 'test_res/resr4.jpg'

# Read in image
img = cv2.imread(f)


# Sharpen the image (unsharpen mask)
blur = cv2.blur(img, (7,1))
cv2.addWeighted(img, 1.5, blur, -0.5, 0, blur)

# Convert to grayscale
gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)



print 'width:', len(img[0])
print 'height:', len(img)
img_width = len(img[0])
img_height = len(img)

#ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
thresh = cv2.Canny(gray, 30, 75)
thresh_y = []
thresh_y_bin = []

print thresh[0, 0]
print thresh[0][0]
print len(thresh)
print len(thresh[0])

# sum threshold in y directions to find peaks
for c in range(0, img_width):
	sum_col = 0
	for r in range(0, img_height):
		# print str(r) + " " + str(c)
		sum_col += thresh[r, c]
	thresh_y.append(sum_col)
	if sum_col > 3000:
		thresh_y_bin.append(1)
	else:
		thresh_y_bin.append(0)
plt.plot(thresh_y)
plt.show()

# increase above 5000 -> walk until below 5000, use middle as cut point
x_cuts = []
start_x = 0
tracing_ones = (thresh_y_bin[0] == 1) 
print len(thresh_y_bin)

for c in range(1, img_width):
	# if tracing_ones and thresh_y_bin[c] == 1:
		# do nothing
	if tracing_ones and thresh_y_bin[c] == 0:
		x_cuts.append(math.floor((start_x + c)/2))
		start_x = c + 1
		tracing_ones = False 
	elif not(tracing_ones) and thresh_y_bin[c] == 1:
		tracing_ones = True;
		start_x = c
    # not tracing ones and found a 0
	elif not(tracing_ones) and thresh_y_bin[c] == 0: 
		start_x = c

print x_cuts
cv2.imshow('thresh', thresh)

top_row = 0
bottom_row = img_height - 1
num_vert_sections = 15

for i in range(0, len(x_cuts) - 1):
	start_x = x_cuts[i]
	end_x = x_cuts[i+1]
	cropped_im = np.array(img[top_row:bottom_row])
	cropped_im = np.array([col[start_x:end_x] for col in cropped_im])

	avg_color = avg_img_color_np(cropped_im)

	min_dist_i = min_distance_index(avg_color)

	print "Start_x:" + str(start_x) + "\t End_x:"+str(end_x)+ "\t" + color_names[min_dist_i]

# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 
# 
# colors = [(255,0,0), 
# (0, 255, 0), 
# (0, 0, 255),
# (255, 255, 0),
# (0, 255, 255),
# (255, 0, 255)]
# 
# """
# # Find the longest contour
# 
# longest = []
# for cnt in contours:
# 	if len(cnt) > len(longest):
# 		longest = cnt
# 
# # Draw the longest contour on the image
# #cv2.drawContours(img, [longest], 0, colors[0], 3)
# """
# 
# # Only allow contours greater than 25
# contours = filter(lambda x: len(x) > 25, contours)
# 
# # Remove contours with greater x variance
# contours = filter(x_var_filter, contours)
# 
# x_means = []
# 
# 
# x_mean_thresh = img_width * 0.03
# # Pair all of the x means for each contour with the contour
# # Filter out contours that are too close
# for new_cnt in contours:
# 	new_mean = np.mean(new_cnt, 0)[0][0]
# 
# 	flagged = False
# 	for x_mean, cnt  in x_means:
# 		if abs(x_mean - new_mean) < x_mean_thresh:
# 			flagged = True
# 
# 	if not flagged:
# 		x_means += [(new_mean, new_cnt)]
# 
# filtered_contours = [ cnt for mean, cnt in x_means]
# 
# 
# for index, cnt in enumerate(filtered_contours):
# 	# Approximate each contour
#     approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt,True), True)
#     #print 'len(approx):', len(approx)
# 
#     #cv2.drawContours(img, [cnt], 0, colors[index % 6], 3)
# 
#     cv2.drawContours(img, [approx], 0, colors[index % 6], 5)
# 
# 
# cv2.imshow('img',img)
#cv2.imshow('gray', gray)


cv2.waitKey(0)
cv2.destroyAllWindows()
