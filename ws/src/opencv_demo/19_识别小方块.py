import cv2 as cv
import numpy as np
img1 = cv.imread("./assets/square.jpg");

roi = img1[250:900,700:1400]




def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    print("d1.dot(d2):",np.dot(d1, d2)," shape:",p0.shape )

    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    squares = []
    circleInfos = []
    rectInfos = []
    for gray in cv.split(img):

            # if thrs == 0:
            #     bin = cv.Canny(gray, 0, 50, apertureSize=5)
            #     bin = cv.dilate(bin, None)
            # else:
        _retval, bin = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
        _,contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv.arcLength(cnt, True)
            cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                print("cnt:",cnt)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
                    # 获取当前轮廓的外切圆
                    circleInfo = cv.minEnclosingCircle(cnt);
                    rect = cv.minAreaRect(cnt);

                    print("rect:",rect)

                    x = int(circleInfo[0][0])
                    y = int(circleInfo[0][1])

                    print(int(x),int(y))

                    circleInfos.append(circleInfo);
                    rectInfos.append(rect);



    return squares,circleInfos,rectInfos

if __name__ == '__main__':
    # img = cv.imread('data/pic10.png')
    squares,circleInfo,rectInfos = find_squares(roi)
    # cv.drawContours( roi, squares, -1, (0, 255, 0), 3)
    # cv.imshow('squares', img)
    cv.imshow("dst",roi);

    for point,radius in circleInfo:
        # print(point,radius);
        cv.circle(roi, (int(point[0]), int(point[1])), int(radius), (0, 0, 255), 2)

    for point,radius in circleInfo:
        # print(point,radius);
        cv.circle(roi, (int(point[0]), int(point[1])), int(radius), (0, 0, 255), 2)

    for rect in rectInfos:
        x = int(rect[0][0])
        y = int(rect[0][1])
        w = int(rect[1][0])
        h = int(rect[1][1])

        cv.rectangle(roi,(x-int(w/2),y-int(h/2)),(x+int(w/2),y+int(h/2)), (0, 255, 255), 2);
        # cv.circle(roi, (int(point[0]), int(point[1])), int(radius), (0, 0, 255), 2)

    # print(len(squares))
    # print(len(circleInfo))
    cv.imshow("dst", roi);
    cv.waitKey(0);