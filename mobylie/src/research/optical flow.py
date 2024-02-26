from mobylie.src.research import videoLoader
import cv2
import numpy as np
import matplotlib.pyplot as plt
from CarDetection import detectCar
from mobylie.src.research.imgDetector import imgDetector
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 420
FOCAL_LENGTH = 27
SENSOR_SIZE = 1 / 2.3

def main():

    loader = videoLoader.VideoLoader("../videos/highway1.mp4")
    loader.nextFrame()
    prevGrayImg=cv2.cvtColor(loader._img._bgrImg,cv2.COLOR_BGR2GRAY)
    loader.nextFrame()
    dettector = imgDetector()
    carRes = detectCar(loader._img._bgrImg)
    dettector.updateCar(carRes)
    grayImg=cv2.cvtColor(loader._img._bgrImg,cv2.COLOR_BGR2GRAY)
    flow=cv2.calcOpticalFlowFarneback(prevGrayImg,grayImg,None,
                                 0.5,3,15,
                                 3,5,1.2,0)
    vx, vy = np.split(flow, 2, axis=-1)
    G = np.hypot(vx, vy)
    for car in dettector.carArray:
        top_left = car.bounding_box.getTopLeftPoint(car.bounding_box.x, car.bounding_box.y, car.bounding_box.width,
                                                    car.bounding_box.length)
        bottom_right = car.bounding_box.getBottomRightPoint(car.bounding_box.x, car.bounding_box.y,
                                                            car.bounding_box.width, car.bounding_box.length)
        intTopLeft = (int(top_left[0]), int(top_left[1]))  # parse from float to int
        intBottomRight = (int(bottom_right[0]), int(bottom_right[1]))  # parse from float to int
        cv2.rectangle(G, intTopLeft, intBottomRight, (0,7,90), 1)
        FOV_angle=2* np.arctan (SENSOR_SIZE / (2* FOCAL_LENGTH))

    while True:
        cv2.imshow("bgr", vy)
        cv2.imshow("hsl", vx)
        cv2.imshow("idk", G)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    main()