import cv2 as cv
import numpy as np;


img = cv.imread("assets/4.png")

cv.imshow("img",img)

gray = cv.cvtColor(img,cv.COLOR_BGRA2GRAY);

cv.imshow("gray",gray);


kernel = np.ones((3,3),np.uint8)
erode = cv.erode(gray,kernel)
cv.imshow("erode",erode);

# r,binary = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
# 直接调用api处理 参数1：图像数据 参数2：最大值  参数3：计算阈值的方法， 参数4：阈值类型 参数5：处理块大小  参数6：算法需要的常量C
thresh_img = cv.adaptiveThreshold(erode,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,5)
cv.imshow("thresh_img",thresh_img)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
dst = cv.morphologyEx(thresh_img, cv.MORPH_OPEN, kernel)
dst = cv.morphologyEx(dst, cv.MORPH_OPEN, kernel)

dst = cv.erode(dst,kernel)
dst = cv.erode(dst,kernel)
dst = cv.dilate(dst,kernel)

cv.imshow("dst",dst)

cv.waitKey(0);