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
        print("i dont know what or how you want to do it we will do it tommorow")

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
