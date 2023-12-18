from mobylie.src.research.obj import Bounding_Box
from mobylie.src.research.obj import General_Object as obj


class imgDetector:
    def __init__(self):
        self.carArray=[]
        self.signArray=[]
        self.ourCar=obj.General_Object(Bounding_Box.Bounding_Box(0,0,0,0),"our_car")
    def updateCar(self,res):
        cars=[]
        objSplited=res.split("\n")
        for objText in objSplited:
            objText=objText.replace("[","")
            objText=objText.replace("]","")
            info=objText.split(",")
            if(len(info)==5):
                box=Bounding_Box.Bounding_Box(int(float(info[0])),
                                              int(float(info[1])),
                                              int(float(info[2])),
                                              int(float(info[3])))#create bounding box
                                                    #name
                cars.append(obj.General_Object(box,info[4]))#add to list
        if(len(self.carArray)>0):
            self.compareList(cars,True)
        else:
            self.copyCarArr(cars)
    def updateSign(self,res):
        signs=[]
        objSplited=res.split("\n")
        for objText in objSplited:
            objText=objText.replace("[","")
            objText=objText.replace("]","")
            info=objText.split(",")
            if(len(info)==5):
               box=Bounding_Box.Bounding_Box(int(float(info[0])),
                                              int(float(info[1])),
                                              int(float(info[2])),
                                              int(float(info[3])))#create bounding box                                     #name
               signs.append(obj.General_Object(box,info[4]))#add to list
        if(len(self.signArray)>0):
            self.compareList(signs,False)
        else:
            self.copySignArr(signs)

    def updateOurCar(self):
        sum = obj.Data(obj.Vec(0,0),obj.Vec(0,0),obj.Vec(0,0))
        posNonZeroCounter = 0
        velNonZeroCounter = 0
        accNonZeroCounter = 0
        #adds them up to have the avg
        for sign in self.signArray:
            if sign.data.position.x != 0 and sign.data.position.y != 0:
                sum.position+=sign.data.position
                posNonZeroCounter+=1
            if sign.data.velocity.x != 0 and sign.data.velocity.y != 0:
                sum.velocity+=sign.data.velocity
                velNonZeroCounter+=1
            if sign.data.aceloration.x != 0 and sign.data.aceloration.y != 0:
                sum.aceloration+=sign.data.aceloration
                posNonZeroCounter+=1
        try:
            #calc avg
            sum.position.x=sum.position.x/posNonZeroCounter
            sum.position.y=sum.position.y/posNonZeroCounter
            self.ourCar.data.position+=sum.position
            self.ourCar.data.velocity.x=sum.velocity.x/velNonZeroCounter
            self.ourCar.data.velocity.y=sum.velocity.y/velNonZeroCounter
            self.ourCar.data.aceloration.x=sum.aceloration.x/accNonZeroCounter
            self.ourCar.data.aceloration.y=sum.aceloration.y/accNonZeroCounter
        except ZeroDivisionError:
            #if there wasnt enough information to calc it
            print("zero info")

    def compareList(self,temp,carVector):
        IUO_THRESHOLD=0.5
        for tempObj in temp:
            if carVector:
                for car in self.carArray:
                    iou=tempObj.bounding_box.calculateIUO(car.bounding_box)
                    if car.name==tempObj.name and iou>=IUO_THRESHOLD:
                        #tempObj.update()
                        break
            else:
                for sign in self.signArray:
                    iou=tempObj.bounding_box.calculateIUO(sign.bounding_box)
                    if sign.name==tempObj.name and iou>=IUO_THRESHOLD:
                        #tempObj.update(sign)
                        break
            if carVector:
                self.copyCarArr(temp)
            else:
                self.copySignArr(temp)
    def copyCarArr(self,temp):
        self.carArray.clear()
        for car in temp:
            self.carArray.append(car)
    def copySignArr(self,temp):
        self.signArray.clear()
        for sign in temp:
            self.carArray.append(sign)
