from CarDetection import detectCar
from SignDetection import detectSign
import imgDetector
import cv2
import videoLoader
import time
import CCA_model as cca
import numpy as np
from mobylie.src.research.database import databaseManger
import math


def main():
    dataManager = databaseManger.Database_Manger("database/database.db")
    dataManager.crateDatabase()
    # i need to copy the y so it will fit
    dictatorX = dataManager.create_dictionary(dataManager.X_TABLE_NAME)
    dictatorY = dataManager.create_dictionary(dataManager.Y_TABLE_NAME)
    predictorX = cca.cca_model(dictatorX)
    predictorY = cca.cca_model(dictatorY)

    loader = videoLoader.VideoLoader("../videos/highway1.mp4")
    dettector = imgDetector.imgDetector()
    while loader.nextFrame():
        start_time = time.time()
        carRes = detectCar(loader._img._bgrImg)
        signRes = detectSign((loader._img._bgrImg))
        dettector.updateCar(carRes)
        dettector.updateSign(signRes)
        dettector.updateOurCar()
        ################################test###################################
        for car in dettector.carArray:
            top_left = car.bounding_box.getTopLeftPoint(car.bounding_box.x, car.bounding_box.y, car.bounding_box.width,
                                                        car.bounding_box.length)
            bottom_right = car.bounding_box.getBottomRightPoint(car.bounding_box.x, car.bounding_box.y,
                                                                car.bounding_box.width, car.bounding_box.length)
            intTopLeft = (int(top_left[0]), int(top_left[1]))  # parse from float to int
            intBottomRight = (int(bottom_right[0]), int(bottom_right[1]))  # parse from float to int
            cv2.rectangle(loader._img._bgrImg, intTopLeft, intBottomRight, (255, 0, 0), 1)

            text = str(int(car.data.position.x)) + " " \
                   + str(int(car.data.position.y)) + " " \
                   + str(int(car.distance))
            text_position = (intTopLeft[0], intBottomRight[1] - 10)
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            text_color = (255, 0, 0)
            text_thickness = 1
            cv2.putText(loader._img._bgrImg, text,
                        text_position, font_face,
                        font_scale, text_color, text_thickness)
        ################################test###################################3

        ########################test############################
        print("-------------------------our car-------------------------------")
        print((dettector.ourCar.data.position.x, dettector.ourCar.data.position.y))
        print((dettector.ourCar.data.velocity.x, dettector.ourCar.data.velocity.y))
        print((dettector.ourCar.data.aceloration.x, dettector.ourCar.data.aceloration.y))
        ########################test############################

        ########################test############################


        cv2.imshow("bgr", loader._img._bgrImg)
        cv2.imshow("hsl", loader._img._hlsImg)
        end_time = time.time()
        print("time:")
        time_passed = end_time - start_time
        print(time_passed)
        print("-------------------prediction-------------------")
        #                                                          time passed
        print(predictorX.predict(cca.cca_model.getValues(dettector, 0, 1)))
        print(predictorY.predict(cca.cca_model.getValues(dettector, 1, 1)))

        if dataManager.collect_data:
            if dataManager.formerXData != 0 and dataManager.formerYData != 0:
                dataManager.insert_Data(dataManager.X_TABLE_NAME, dataManager.formerXData[0],
                                        dettector.ourCar.data.position.x - dataManager.formerXData[1])
                dataManager.insert_Data(dataManager.Y_TABLE_NAME, dataManager.formerYData[0],
                                        dettector.ourCar.data.position.y - dataManager.formerYData[1])
            dataManager.formerXData = (
                cca.cca_model.getValues(dettector, 0, time_passed)
                , dettector.ourCar.data.position.x)
            dataManager.formerYData = (
                cca.cca_model.getValues(dettector, 1, time_passed)
                , dettector.ourCar.data.position.y)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
