import cv2 as cv
import numpy as np

from svgpathtools import svg2paths2
# paths, attributes, svg_attributes = svg2paths2('drawing.svg')
paths, attributes, svg_attributes = svg2paths2('./assets/test/6.svg')

print(paths,attributes);
#
# for k, v in enumerate(attributes):
#     print(k,v)


# 三 P1*t^3 + P2*3*t^2*(1-t) + P3*3*t*(1-t)^2 + P4*(1-t)^3 = Pnew 
def BerzierCurve3(u ,p1,p2,p3,p4):
    a = np.power(u,3)*p1; #pointTimes(pow(u,3), p[0]);
    b = (3*np.power(u,2)*(1-u))*p2; #pointTimes(3*pow(u,2)*(1-u), p[1]);
    c = (3*u*np.power((1-u),2))*p3; #pointTimes(3*u*pow((1-u),2), p[2]);
    d = np.power((1-u),3)*p4; #pointTimes(pow((1-u),3), p[3]); 
    r = np.add(np.add(a,b),np.add(c,d))
    return r;


# 二阶贝塞尔曲线
# 公式 点= （1-t）^2 *P1 + 2*t(1-t)*P2 + t^2*P3
def BerzierCurve2(t,p1,p2,p3):
    a = np.power((1-t),2)*p1;
    b = 2*t*(1-t)*p2
    c = np.power(t,2)*p3;

    return np.add(np.add(a,b),c);


dst = np.zeros((1080,1920,3),np.uint8);

pre = (0, 0);
# print the line draw commands
for path in paths:
    # path = parse_path(path_string)


    for e in path:
        # print(e)
        if type(e).__name__ == "Move":
             # print(e.start.real,"  ",e.start.imag);
             # x0 = e.start.real
             # y0 = e.start.imag
             # x1 = e.end.real
             # y1 = e.end.imag
             # print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
             pre = (int(e.start.real),int(e.start.imag));
             b = np.random.randint(0, 255)
             g = np.random.randint(0, 255)
             r = np.random.randint(0, 255)
             cv.line(dst,pre, pre, (b, g, r), 1);
        elif type(e).__name__ == 'CubicBezier':
            p1 = np.array([e.start.real,e.start.imag])
            p2 = np.array([e.control1.real,e.control1.imag])
            p3 = np.array([e.control2.real,e.control2.imag])
            p4 = np.array([e.end.real,e.end.imag])

            r = BerzierCurve3(0, p1, p2, p3, p4)
            pre = (int(r[0]),int(r[1]))
            for i in range(1,40):
                u = i/40;
                r = BerzierCurve3(u, p1, p2, p3, p4)
                x = int(r[0])
                y = int(r[1])
                cur=(x,y);

                b = np.random.randint(0, 255)
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                # cv.waitKey(5)
                # cv.imshow("dst", dst);
                cv.line(dst,pre,cur,(b,g,r),1);
                pre = cur


        elif type(e).__name__ == 'QuadraticBezier':
            p1 = np.array([e.start.real, e.start.imag])
            p2 = np.array([e.control.real, e.control.imag])
            p3 = np.array([e.end.real, e.end.imag])

            r = BerzierCurve2(0, p1, p2, p3)
            pre = (int(r[0]), int(r[1]))
            for i in range(1, 40):
                u = i / 40;
                r = BerzierCurve2(u, p1, p2, p3)
                x = int(r[0])
                y = int(r[1])
                cur = (x, y);

                b = np.random.randint(0, 255)
                g = np.random.randint(0, 255)
                r = np.random.randint(0, 255)
                # cv.waitKey(5)
                # cv.imshow("dst", dst);
                cv.line(dst, pre, cur, (b, g, r), 1);
                pre = cur


        elif type(e).__name__ == 'Line':
            x0 = e.start.real
            y0 = e.start.imag
            x1 = e.end.real
            y1 = e.end.imag
            print("(%.2f, %.2f) - (%.2f, %.2f)" % (x0, y0, x1, y1))
            b = np.random.randint(0, 255)
            g = np.random.randint(0, 255)
            r = np.random.randint(0, 255)
            cv.line(dst,(int(x0),int(y0)),(int(x1),int(y1)),(b,g,r),1);
            pre = (int(x1),int(y1))

        cv.waitKey(5);
        cv.imshow("dst", dst);



cv.waitKey(0)