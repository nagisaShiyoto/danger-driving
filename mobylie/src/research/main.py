from CarDetection import detectCar
from SignDetection import detectSign
import cv2
def main():
    print(detectCar(cv2.imread("tempFile.png")))
    print(detectSign(cv2.imread("tempFile.png")))
if __name__ == '__main__':
    main()
