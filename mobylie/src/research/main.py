from CarDetection import detectCar
from SignDetection import detectSign
import cv2
import videoLoader

def main():
    loader=videoLoader.VideoLoader("../videos/highway1.mp4")
    while(loader.nextFrame()):
        cv2.imshow("bgr",loader._img._bgrImg)
        cv2.imshow("hsl",loader._img._hlsImg)
        if cv2.waitKey(1) == ord('q'):
            break
        print("hi")
if __name__ == '__main__':
    main()
