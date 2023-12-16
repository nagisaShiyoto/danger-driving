from detect import detectCar
import cv2
def main():
    print(detectCar(cv2.imread("tempFile.png")))
if __name__ == '__main__':
    main()