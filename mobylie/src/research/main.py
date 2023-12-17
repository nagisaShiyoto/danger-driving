from CarDetection import detectCar
from SignDetection import detectSign
import imgDetector
import cv2
import videoLoader

def main():
    loader=videoLoader.VideoLoader("../videos/highway1.mp4")
    dettector=imgDetector.imgDetector()
    while(loader.nextFrame()):
        res=detectCar(loader._img._bgrImg)
        dettector.updateCar(res)
        cv2.imshow("bgr",loader._img._bgrImg)
        cv2.imshow("hsl",loader._img._hlsImg)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    main()
