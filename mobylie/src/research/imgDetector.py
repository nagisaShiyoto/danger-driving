# from src.research.obj import Bounding_Box
# from src.research.obj import General_Object as obj
from mobylie.src.research.obj import Bounding_Box
from mobylie.src.research.obj import General_Object as obj

import segmentation as seg
from CarDetection import detectCar
from SignDetection import detectSign

import numpy as np
import cv2


class Statistics:
    # the data can use another check, but these are the base values I found.d
    NOT_IN_DATA_FLAG = -1
    DATA = {"truck": 5, "car": 2.6, "line": 1.5}  # the avg height of clavicles in meters

    @staticmethod
    def getHeight(type):
        """
        return the avg height according to type
        input: type-the name of the obj
        output: the height in meters(or -1 if not found)
        """
        NOT_IN_DATA_FLAG = -1
        try:
            return Statistics.DATA[type]
        except KeyError:
            return NOT_IN_DATA_FLAG


class imgDetector:
    def __init__(self,img_config,showObjectsData):
        """
        create the detector
        input:img_config-configuration_data
            showObjectsData-flag to print all the real life data of objects
        output:none
        """
        self.carArray = []
        self.staticObjArray = []
        self.img_data = (img_config["image width"], img_config["image height"],
                         img_config["FOCAL LENGTH"], img_config["SENSOR SIZE"])
        self.ourCar = obj.General_Object(Bounding_Box.Bounding_Box(0, 0, 0, 0),
                                         "our_car",self.img_data)
        self.showObjectsData=showObjectsData

    def updateCar(self, res):
        """
        update the cars' data and the array
        input: res-string of all the dettected cars
        output:none
        """
        cars = []
        objSplited = res.split("\n")
        for objText in objSplited:
            # split the data so we could read it
            objText = objText.replace("[", "")
            objText = objText.replace("]", "")
            info = objText.split(",")

            # create a bounding box from the data
            if len(info) == 5:
                box = Bounding_Box.Bounding_Box(int(float(info[0])),
                                                int(float(info[1])),
                                                int(float(info[2])),
                                                int(float(info[3])))
                # name
                cars.append(obj.General_Object(box, info[4],self.img_data))  # add to list
        # compare the vehicle array to the last array for velocoty and acceleration calc
        if (len(self.carArray) > 0):
            self.compareList(cars, True)
        else:
            self.copyCarArr(cars)

    def aCar(self, obj, threshold):
        """check if the found obj is a car
        input:obj-the obj to check
            threshold - amount of ceternteny which above counts as a car
        output:true-car,false-not car"""
        for car in self.carArray:
            if (car.bounding_box.calculateIUO(obj.bounding_box) >= threshold):
                return True
        return False

    def updateStaticObj(self, res):
        """
        update the static objs' data and the array
        input: res-string of all the dettected cars
        output:none
        """
        signs = []
        objSplited = res.split("\n")
        for objText in objSplited:
            # split the data so we could read it
            objText = objText.replace("[", "")
            objText = objText.replace("]", "")
            info = objText.split(",")

            # create a bounding box from the data
            if len(info) == 5:
                box = Bounding_Box.Bounding_Box(int(float(info[0])),
                                                int(float(info[1])),
                                                int(float(info[2])),
                                                int(float(info[
                                                              3])))  # create bounding box                                     #name
                line = obj.General_Object(box, info[4],self.img_data)
                # check if the obj is not a part of a car
                if not self.aCar(line, 0.8) and line.distance != 0:
                    signs.append(line)  # add to list

        # compare the vehicle array to the last array for velocoty and acceleration calc
        if len(self.staticObjArray) > 0:
            self.compareList(signs, False, 0.5)
        else:
            self.copySignArr(signs)

    @staticmethod
    def calcDistanceWay1(objectName, boundingBox, img_data,max_dis=5):
        """
        calc the real life distance in meters
        input:objectName-the type name for hight
            bounding_box- the plcae and size of the obj in pic
            img_data-data for the forumela
        output:real life distance in meters
        """
        if (boundingBox.y < 310):
            IMAGE_HEIGHT=img_data[0]
            IMAGE_WIDTH=img_data[1]
            SENSOR_SIZE=img_data[2]
            FOCAL_LENGTH=img_data[3]
            num_of_pixels = IMAGE_HEIGHT * IMAGE_WIDTH
            objHight = Statistics.getHeight(objectName)
            if (objHight == Statistics.NOT_IN_DATA_FLAG):
                return Statistics.NOT_IN_DATA_FLAG
            dis = (FOCAL_LENGTH * objHight * SENSOR_SIZE * num_of_pixels) / (
                    boundingBox.length * IMAGE_HEIGHT * 100.0)
            if objectName == "line" and dis > max_dis:
                return 0
            return dis
        else:
            return 0

    def updateOurCar(self):
        """
        update the data on our car from the static obj
        input:none
        output:none
        """
        sum = obj.Data(obj.Vec(0, 0), obj.Vec(0, 0), obj.Vec(0, 0))
        posNonZeroCounter = 0
        velNonZeroCounter = 0
        accNonZeroCounter = 0 # creating the vectors for calculation

        if (len(self.staticObjArray) == 0):
            return
        # adds them up to have the avg
        for sign in self.staticObjArray:
            # adds negetive becuase static obj have opposite vel
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

    def compareList(self, temp, carVector, IUO_THRESHOLD=0.6):
        """
        compare the objects from the last array to find same objects
         and to calc velocity and acceleration
        input: temp - the recent vector of the object
            carVector - flag to symbolise which vector to compare to
                        true,car vector false-static obj
            IUO_THRESHOLD-the amount of certenty which above count as the same obj
        output:none
        """
        for tempObj in temp:
            if carVector:
                for car in self.carArray:
                    # check if the same obj
                    iou = tempObj.bounding_box.calculateIUO(car.bounding_box)
                    if car.name == tempObj.name and iou >= IUO_THRESHOLD:
                        tempObj.update(car,self.showObjectsData)
                        break
            else:
                for sign in self.staticObjArray:
                    # check if the same obj
                    iou = tempObj.bounding_box.calculateIUO(sign.bounding_box)
                    if sign.name == tempObj.name and iou >= IUO_THRESHOLD:
                        tempObj.update(sign,self.showObjectsData)
                        break
        if carVector:
            self.copyCarArr(temp)
        else:
            self.copySignArr(temp)

    def copyCarArr(self, temp):
        """
        copy the car temp array to the array of the dettector
        input:temp-the array to copy
        output:none
        """
        self.carArray.clear()
        for car in temp:
            self.carArray.append(car)

    def copySignArr(self, temp):
        """
        copy the staticObj temp array to the array of the dettector
        input:temp-the array to copy
        output:none
        """
        self.staticObjArray.clear()
        for sign in temp:
            self.staticObjArray.append(sign)

    def dettect(self, img):
        """
        dettect all the objects in an img
        input:img-the img to detect from
        output:none
        """
        self.carDettection(img)
        self.nonMovingObjDettection(img)
        self.updateOurCar()

    def carDettection(self, img):
        """
        detect cars from img
        input:img-the img to detect from
        output:none
        """
        carString = detectCar(img)  # yolo detection
        self.updateCar(carString)  # put it in a vec

    def nonMovingObjDettection(self, img):
        """
        detect staticObj from img
        input:img-the img to detect from
        output:none
        """
        signRes = detectSign(img)  # yolo detection
        signRes += "\n" + seg.dettect(img)  # seg detection
        self.updateStaticObj(signRes)  # put it in a vec

    @staticmethod
    def alertUser(time, carVector, predX, predY,X_RANGE = 5,Y_RANGE = 2):
        """
        check if you need to allert the user from a danger
        input: time-amount of time the pred
                carVector-the vec to check from coliding
                predX,predY-the predictions
                X_RANGE,Y_RANGE-the range where it counts coliding
        """
        for car in carVector:
            #phisics pred on all cars
            x = (car.data.position.x +
                 car.data.velocity.x * time +
                 0.5 * car.data.aceloration.x * time * time)
            y = (car.data.position.y +
                 car.data.velocity.y * time +
                 0.5 * car.data.aceloration.y * time * time)
            if (x - X_RANGE) >= predX[0]:
                return True
            if (y - Y_RANGE) >= predY[0] and (y + Y_RANGE) <= predY[0]:
                return True
        return False

    def printOurCarInfo(self):
        """
        print the data  of our car
        input:none
        output:none
        """
        print("-------------------------our car-------------------------------")
        print((self.ourCar.data.position.x, self.ourCar.data.position.y))
        print((self.ourCar.data.velocity.x, self.ourCar.data.velocity.y))
        print((self.ourCar.data.aceloration.x, self.ourCar.data.aceloration.y))
        print("-------------------------our car-------------------------------")
