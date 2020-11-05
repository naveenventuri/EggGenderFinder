# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:57:49 2020

@author: prasa
"""
import cv2
import numpy as np
import operator
import math

I=cv2.imread('Input/egg_flash.jpeg')
contour = np.copy(I)

cv2.imshow("Original Image",I)
gray = cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)

cv2.imshow("GrayScale Image",gray)
cv2.imwrite("Output/Grayscale.jpg",gray)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imshow("Threshold Image",thresh)
cv2.imwrite("Output/Seperation.jpg",thresh)
points = zip(*np.where(thresh == 0))

#distance = math.sqrt( ((min(x)-max(x))**2)+((min(y)-max(y))**2) )

#cv2.line(thresh,(points[0][0],points[0][1]),(points[-1][0],points[-1][1]),(0,255,255),12)

row_sort = list(points)


col_sort = sorted(row_sort,key = operator.itemgetter(1))


res ={}


for point in row_sort:
    if point[0] in res:
        res[point[0]]=(*res[point[0]],*point[1:])
    else:
        res[point[0]]=point
        

least = res[row_sort[0][0]]
highest = res[row_sort[-1][0]]

dist_1 = math.sqrt(((least[1]-highest[-1])**2)+((least[0]-highest[0])**2))
dist_2 = math.sqrt(((least[-1]-highest[1])**2)+((least[0]-highest[0])**2))

point_1=[]
point_2=[]
if dist_1 > dist_2:
    cv2.line(I,(least[1],least[0]),(highest[-1],highest[0]),(255,0,0),2)
    point_1.append((least[0],least[1]))
    point_2.append((highest[0],highest[-1]))
else:
    cv2.line(I,(least[-1],least[0]),(highest[1],highest[0]),(255,0,0),2)
    point_1.append((least[0],least[-1]))
    point_2.append((highest[0],highest[1]))
    

point_3=[]
point_4=[]
res_2 ={}

rev_col_sort = [point[::-1] for point in col_sort]
for point in rev_col_sort:
    if point[0] in res_2:
        res_2[point[0]]=(*res_2[point[0]],*point[1:])
    else:
        res_2[point[0]]=point
        

least_2 = res_2[rev_col_sort[0][0]]
highest_2 = res_2[rev_col_sort[-1][0]]

dist_3 = math.sqrt(((least_2[1]-highest_2[-1])**2)+((least_2[0]-highest_2[0])**2))
dist_4 = math.sqrt(((least_2[-1]-highest_2[1])**2)+((least_2[0]-highest_2[0])**2))


if dist_3 > dist_4:
    cv2.line(I,(least_2[0],least_2[1]),(highest_2[0],highest_2[-1]),(255,0,0),2)
    point_3.append((least_2[1],least_2[0]))
    point_4.append((highest_2[-1],highest_2[0]))
else:
    cv2.line(I,(least_2[0],least_2[-1]),(highest_2[0],highest_2[1]),(255,0,0),2)
    point_3.append((least_2[-1],least_2[0]))
    point_4.append((highest_2[1],highest_2[0]))


for i in range(1,len(least)):
    contour[least[0]][least[i]] = 0

for i in range(1,len(highest)):
    contour[highest[0]][highest[i]] = 0

for i in range(1,len(least_2)):
    contour[least_2[i]][least_2[0]] = 0

for i in range(1,len(highest_2)):
    contour[highest_2[i]][highest_2[0]] = 0

#cnt_points = np.where(thresh[500]==0)
for i in range(len(thresh)):
    cnt_points = np.where(thresh[i]==0)
    if (len(cnt_points[0])>0):
       contour[i][min(cnt_points[0])]=0
       contour[i][max(cnt_points[0])]=0
    
cv2.imshow("Contout Image",contour)
cv2.imwrite("Output/Contour.jpg",contour)
    
cv2.imshow("Line Image",I)
cv2.imwrite("Output/Lines.jpg",I)
cv2.waitKey(0)



