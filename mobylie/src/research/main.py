import numpy as np
import imgDetector
import cv2
import videoLoader
import time
import CCA_model as CCA
import kalman_filter
import json

# Eylon's imports:
from mobylie.src.research.database import databaseManger


# Yotam's imports:
# from src.research.database import databaseManger

def show_data(loader, detector, time_passed, kfX, kfY, Zx, Zy):
    # functions to better see the object detection:
    if loader.config_data["data"]["car detection"]:
        loader.showObjects(detector.carArray, loader.config_data["coloring options"]["cars color"])
    if loader.config_data["data"]["static objects detection"]:
        loader.showObjects(detector.staticObjArray, loader.config_data["coloring options"]["static objects color"])
    if loader.config_data["data"]["show ourCar data"]:
        detector.printOurCarInfo()
    if loader.config_data["data"]["show rgb img"]:
        cv2.imshow("bgr", loader._img._bgrImg)
    if loader.config_data["data"]["show hls img"]:
        cv2.imshow("hsl", loader._img._hlsImg)
    if loader.config_data["data"]["show detection time"]:
        print("time:")
        print(time_passed)
    if loader.config_data["data"]["alert user"] \
            and imgDetector.imgDetector.alertUser(1,
                                                  detector.carArray,
                                                  kfX.X,
                                                  kfY.X):
        print("the car needs to slow down!")
    if loader.config_data["data"]["show prediction"]:
        print("================== pred =====================")
        print(kfX.X, kfY.X)
        print(Zx, Zy)
        print("================== pred =====================")


def main():
    # creating the video loader
    loader = videoLoader.VideoLoader()
    loader.nextFrame()  # so it will have prevImg

    # creating the image detector
    detector = imgDetector.imgDetector(
        loader.config_data["calculating info"],
        loader.config_data["data"]["show obj Data"])

    # Data base management
    dataManager = databaseManger.Database_Manger("database/database.db",loader.config_data["data"]["collects data"])  # opening the database
    dictionary_X = dataManager.create_dictionary(dataManager.X_TABLE_NAME)
    dictionary_Y = dataManager.create_dictionary(dataManager.Y_TABLE_NAME)

    # CCA model creation
    predictorX = CCA.cca_model(dictionary_X,loader.config_data["data"]["show x graph"])
    predictorY = CCA.cca_model(dictionary_Y,loader.config_data["data"]["show y graph"])

    # kalman model creation
    kfX = kalman_filter.KalmanFilter(  # kalman filter for the x axis
        # https://www.fxp.co.il
        np.array([[1, 1, 0.5], [0, 1, 1], [0, 0, 1]]),  # f
        [[0.2, 0.3, 0.35], [0, 0.3, 0.35], [0, 0, 0.35]],  # the certainty percentage
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],  # to adjust the matrix
        [0, 0, 0],  # will change every time
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # will change every time
        [[predictorX.certentry, 1, 1], [1, predictorX.certentry, 1], [1, 1, predictorX.certentry]]
        # certainty percentage of CCA
    )

    kfY = kalman_filter.KalmanFilter(  # kalman filter for the y axis
        # https://www.fxp.co.il
        np.array([[1, 1, 0.5], [0, 1, 1], [0, 0, 1]]),  # f
        [[0.2, 0.3, 0.35], [0, 0.3, 0.35], [0, 0, 0.35]],  # the certainty percentage
        [[1, 0, 0], [1, 0, 0], [1, 0, 0]],  # to adjust the matrix
        [0, 0, 0],  # will change every time
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # will change every time
        [[predictorX.certentry, 1, 1], [1, predictorX.certentry, 1], [1, 1, predictorX.certentry]]
        # the
        # certainty percentage of CCA
    )

    # the loop that runs on the video
    while loader.nextFrame():
        start_time = time.time()  # creating a global clock for the video to use
        detector.dettect(loader._img._bgrImg)

        # the prediction calculations
        Zx = predictorX.predict(CCA.cca_model.getValues(detector, 0, 1))
        Zy = predictorY.predict(CCA.cca_model.getValues(detector, 1, 1))
        kfX.predict([Zx, 0, 0])
        kfY.predict([Zy, 0, 0])

        # calc the time
        end_time = time.time()
        time_passed = end_time - start_time

        show_data(loader, detector, time_passed, kfX, kfY, Zx, Zy)

        kfX.update([detector.ourCar.data.position.x,
                    detector.ourCar.data.velocity.x,
                    detector.ourCar.data.aceloration.x])
        kfY.update([detector.ourCar.data.position.y,
                    detector.ourCar.data.velocity.y,
                    detector.ourCar.data.aceloration.y])

        if loader.config_data["data"]["collects data"]:
            dataManager.save_Data(detector, time_passed)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
