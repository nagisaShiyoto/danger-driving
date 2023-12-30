#from src.research.obj import Bounding_Box
#from src.research.obj import General_Object as obj
from mobylie.src.research.obj import Bounding_Box
from mobylie.src.research.obj import General_Object as obj


class imgDetector:
    def __init__(self):
        self.carArray = []
        self.signArray = []
        self.ourCar = obj.General_Object(Bounding_Box.Bounding_Box(0, 0, 0, 0), "our_car")

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

    def updateSign(self, res):
        signs = []
        objSplited = res.split("\n")
        for objText in objSplited:
            objText = objText.replace("[", "")
            objText = objText.replace("]", "")
            info = objText.split(",")
            if (len(info) == 5):
                box = Bounding_Box.Bounding_Box(int(float(info[0])),
                                                int(float(info[1])),
                                                int(float(info[2])),
                                                int(float(info[
                                                              3])))  # create bounding box                                     #name
                signs.append(obj.General_Object(box, info[4]))  # add to list
        if len(self.signArray) > 0:
            self.compareList(signs, False)
        else:
            self.copySignArr(signs)
    def calcDistanceWay1(self, pixels_length, real_length):
        focal_length=24
        return ((focal_length * pixels_length) / 1300)
    def updateOurCar(self):
        sum = obj.Data(obj.Vec(0, 0), obj.Vec(0, 0), obj.Vec(0, 0))
        posNonZeroCounter = 0
        velNonZeroCounter = 0
        accNonZeroCounter = 0
        # adds them up to have the avg
        for sign in self.carArray:
            if sign.distanceBetweenTwoFrames.x != 0 or sign.distanceBetweenTwoFrames.y != 0:
                sum.position.x += sign.distanceBetweenTwoFrames.x
                sum.position.y += sign.distanceBetweenTwoFrames.y
                posNonZeroCounter += 1
            if sign.data.velocity.x != 0 or sign.data.velocity.y != 0:
                sum.velocity.x += sign.data.velocity.x
                sum.velocity.y += sign.data.velocity.y
                velNonZeroCounter += 1
            if sign.data.aceloration.x != 0 or sign.data.aceloration.y != 0:
                sum.aceloration.x += sign.data.aceloration.x
                sum.aceloration.y += sign.data.aceloration.y
                accNonZeroCounter += 1
        try:
            # calc avg
            if posNonZeroCounter != 0:
                sum.position.x = sum.position.x / posNonZeroCounter
                sum.position.y = sum.position.y / posNonZeroCounter
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

    def compareList(self, temp, carVector):
        IUO_THRESHOLD = 0.6
        for tempObj in temp:
            if carVector:
                for car in self.carArray:
                    iou = tempObj.bounding_box.calculateIUO(car.bounding_box)
                    if car.name == tempObj.name and iou >= IUO_THRESHOLD:
                        tempObj.update(car)
                        print(tempObj.id)
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
            self.carArray.append(sign)
