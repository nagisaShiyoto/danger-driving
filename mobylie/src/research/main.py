from CarDetection import detectCar
from SignDetection import detectSign
import imgDetector
import cv2
import videoLoader
import time

def main():
    loader=videoLoader.VideoLoader("../videos/highway1.mp4")
    dettector=imgDetector.imgDetector()
    while(loader.nextFrame()):
        start_time=time.time()
        carRes=detectCar(loader._img._bgrImg)
        signRes=detectSign((loader._img._bgrImg))
        dettector.updateCar(carRes)
        dettector.updateSign(signRes)
        ################################test###################################
        for car in dettector.carArray:

            top_left=car.bounding_box.getTopLeftPoint(car.bounding_box.x,car.bounding_box.y,car.bounding_box.width,car.bounding_box.length)
            bottom_right=car.bounding_box.getBottomRightPoint(car.bounding_box.x,car.bounding_box.y,car.bounding_box.width,car.bounding_box.length)
            intTopLeft=(int(top_left[0]),int(top_left[1]))#parse from float to int
            intBottomRight=(int(bottom_right[0]),int(bottom_right[1]))#parse from float to int
            cv2.rectangle(loader._img._bgrImg,intTopLeft,intBottomRight,(255,0,0),1)

            text_position = (intTopLeft[0], intBottomRight[1]-10)
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            text_color = (255, 0, 0)
            text_thickness = 1
            cv2.putText(loader._img._bgrImg, car.name,
                        text_position, font_face,
                        font_scale, text_color, text_thickness)
        ################################test###################################3


        end_time=time.time()
        print("time:")
        print(end_time-start_time)



        cv2.imshow("bgr",loader._img._bgrImg)
        cv2.imshow("hsl",loader._img._hlsImg)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    main()
