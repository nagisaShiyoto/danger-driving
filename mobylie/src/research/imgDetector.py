# from src.research.obj import Bounding_Box
# from src.research.obj import General_Object as obj
from mobylie.src.research.obj import Bounding_Box
from mobylie.src.research.obj import General_Object as obj

import numpy as np
import cv2
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 420
FOCAL_LENGTH = 27
SENSOR_SIZE = 1 / 2.3


class Statistics:
    # the data can use another check, but these are the base values I found.
    NOT_IN_DATA_FLAG = -1
    DATA = {"truck": 2.7, "car": 1.6,"line":3}  # the avg height of clavicles in meters

    @staticmethod
    def getHeight(type):

        try:
            return Statistics.DATA[type]
        except KeyError:
            return -1


class imgDetector:
    def __init__(self):
        self.carArray = []
        self.signArray = []
        self.ourCar = obj.General_Object(Bounding_Box.Bounding_Box(0, 0, 0, 0), "our_car")


    def calcOpticalFlow(self,prev, now):
        prevGrayImg = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        grayImg = cv2.cvtColor(now, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevGrayImg, grayImg, None,
                                            0.5, 3, 15,
                                            3, 5, 1.2, 0)
        vx, vy = np.split(flow, 2, axis=-1)
        self.opticalFlow=np.hypot(vx,vy)

    @staticmethod
    def calcPixelCm_ratio(movedCm,movedPixels):
        return movedCm*100/float(movedPixels)

    def calcway(self,ratio):
        x=np.abs(np.max(self.opticalFlow)*ratio[0]/1000)
        return x
    def calcAvgRatio(self):
        sumRatioY=0
        sumRatioX=0
        arraySize=0
        for car in self.carArray:
            sumRatioY += imgDetector.calcPixelCm_ratio(car.distanceBetweenTwoFrames.y,
                                                    self.opticalFlow[car.bounding_box.x][car.bounding_box.y])
            arraySize+=1
        return (
            (sumRatioX/arraySize)
            ,(sumRatioY/arraySize)
        )

    def updateCar(self, res):
        cars = []
        objSplited = res.split("\n")
        for objText in objSplited:
            objText = objText.replace("[", "")
            objText = objText.replace("]", "")
            info = objText.split(",")
            if len(info) == 5:
                box = Bounding_Box.Bounding_Box(int(float(info[0])),
                                                int(float(info[1])),
                                                int(float(info[2])),
                                                int(float(info[3])))  # create bounding box
                # name
                cars.append(obj.General_Object(box, info[4]))  # add to list
        if (len(self.carArray) > 0):
            self.compareList(cars, True)
        else:
            self.copyCarArr(cars)
    def aCar(self,obj,threshold):
        for car in self.carArray:
            if(car.bounding_box.calculateIUO(obj.bounding_box)>=threshold):
                return True
        return False
    def updateSign(self, res):
        signs = []
        objSplited = res.split("\n")
        for objText in objSplited:
            objText = objText.replace("[", "")
            objText = objText.replace("]", "")
            info = objText.split(",")
            if len(info) == 5:
                box = Bounding_Box.Bounding_Box(int(float(info[0])),
                                                int(float(info[1])),
                                                int(float(info[2])),
                                                int(float(info[
                                                              3])))  # create bounding box                                     #name
                line=obj.General_Object(box, info[4])
                if not self.aCar(line,0.8):
                    signs.append(line)# add to list

        if len(self.signArray) > 0:
            self.compareList(signs, False,0.5)
        else:
            self.copySignArr(signs)

    # calc the distance in cm probably
    @staticmethod
    def calcDistanceWay1(objectName, boundingBox):
        if(boundingBox.y<310):
            num_of_pixels = IMAGE_HEIGHT * IMAGE_WIDTH
            objHight = Statistics.getHeight(objectName)
            if (objHight == Statistics.NOT_IN_DATA_FLAG):
                return Statistics.NOT_IN_DATA_FLAG
            dis= (FOCAL_LENGTH * objHight * SENSOR_SIZE * num_of_pixels) / (
                    boundingBox.getLength() * IMAGE_HEIGHT * 100.0)
            if objectName=="line" and dis>15:
                return 0
            return dis
        else:
            return 0

    def updateOurCar(self):
        sum = obj.Data(obj.Vec(0, 0), obj.Vec(0, 0), obj.Vec(0, 0))
        posNonZeroCounter = 0
        velNonZeroCounter = 0
        accNonZeroCounter = 0
        if(len(self.signArray)==0):
            return
        # adds them up to have the avg
        for sign in self.signArray:
            if sign.distanceBetweenTwoFrames.x <= 0 or sign.distanceBetweenTwoFrames.y <= 0:
                sum.position.x += (-sign.distanceBetweenTwoFrames.x)
                sum.position.y += (-sign.distanceBetweenTwoFrames.y)
                posNonZeroCounter += 1
            if sign.data.velocity.x != 0 or sign.data.velocity.y != 0:

                sum.velocity.x += (-sign.data.velocity.x)
                sum.velocity.y += (-sign.data.velocity.y)
                velNonZeroCounter += 1
            if sign.data.aceloration.x != 0 or sign.data.aceloration.y != 0:
                sum.aceloration.x += (-sign.data.aceloration.x)
                sum.aceloration.y += (-sign.data.aceloration.y)
                accNonZeroCounter += 1
        try:
            # calc avg
            if posNonZeroCounter != 0:
                sum.position.x += sum.position.x / posNonZeroCounter
                sum.position.y += sum.position.y / posNonZeroCounter
                self.ourCar.data.position.x += sum.position.x
                self.ourCar.data.position.y += sum.position.y
            if velNonZeroCounter != 0:
                self.ourCar.data.velocity.x = sum.velocity.x / velNonZeroCounter
                self.ourCar.data.velocity.y = sum.velocity.y / velNonZeroCounter
            if accNonZeroCounter != 0:
                self.ourCar.data.aceloration.x = sum.aceloration.x / accNonZeroCounter
                self.ourCar.data.aceloration.y = sum.aceloration.y / accNonZeroCounter
        except ZeroDivisionError:
            print("devided by zero")

    def compareList(self, temp, carVector,IUO_THRESHOLD = 0.6):
        for tempObj in temp:
            if carVector:
                for car in self.carArray:
                    iou = tempObj.bounding_box.calculateIUO(car.bounding_box)
                    if car.name == tempObj.name and iou >= IUO_THRESHOLD:
                        tempObj.update(car)
                        break
            else:
                for sign in self.signArray:
                    iou = tempObj.bounding_box.calculateIUO(sign.bounding_box)
                    if sign.name == tempObj.name and iou >= IUO_THRESHOLD:
                        tempObj.update(sign)
                        break
        if carVector:
            self.copyCarArr(temp)
        else:
            self.copySignArr(temp)

    def copyCarArr(self, temp):
        self.carArray.clear()
        for car in temp:
            self.carArray.append(car)

    def copySignArr(self, temp):
        self.signArray.clear()
        for sign in temp:
            self.signArray.append(sign)

    @staticmethod
    def alertUser(time, carVector, predX, predY):
        X_RANGE = 5
        Y_RANGE = 2
        for car in carVector:
            x = (car.data.position.x +
                 car.data.velocity.x * time +
                 0.5 * car.data.aceloration.x * time * time)
            y = (car.data.position.y +
                 car.data.velocity.y * time +
                 0.5 * car.data.aceloration.y * time * time)
            if (x - X_RANGE) >= predX[0] :
                return True
            if (y - Y_RANGE) >= predY[0] and (y + Y_RANGE) <= predY[0]:
                return True
        return False
