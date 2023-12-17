class obj:
    def __init__(self, objInfo):
        self.name=objInfo[4]
        self.x=int(float(objInfo[0]))
        self.y=int(float(objInfo[1]))
        self.width=int(float(objInfo[2]))
        self.hight=int(float(objInfo[3]))

class imgDetector:
    def __init__(self):
        self.carArray=[]
        self.signArray=[]
        self.ourCar=obj(['0','0','0','0','ourCar'])
    def updateCar(self,res):
        cars=[]
        objSplited=res.split("\n")
        for objText in objSplited:
            objText=objText.replace("[","")
            objText=objText.replace("]","")
            info=objText.split(",")
            if(len(info)==5):
                cars.append(obj(info))
        if(len(self.carArray)>0):
            self.compareList(cars,True)
        else:
            self.carArray=cars
    def updateSign(self,res):
        signs=[]
        objSplited=res.split("\n")
        for objText in objSplited:
            objText=objText.replace("[","")
            objText=objText.replace("]","")
            info=objText.split(",")
            if(len(info)==5):
                signs.append(obj(info))
        if(len(self.signArray)>0):
            self.compareList(signs,False)
        else:
            self.carArray=signs

    def updateOurCar(self):
        print("i dont know what or how you want to do it we will do it tommorow")

    def compareList(self,temp,carVector):
        float IUO_THRESHOLD=0.5
        for obj in temp:
            if carVector:
                for car in self.carArray:
                    iou=obj.calcIOU(car)
                    if car.name==obj.name and iou>=IUO_THRESHOLD:
                        obj.update(car)
                        break;
            else:
                for sign in self.signArray:
                    iou=obj.calcIOU(sign)
                    if sign.name==obj.name and iou>=IUO_THRESHOLD:
                        obj.update(sign)
                        break;
            if carVector:
                self.carArray=temp
            else:
                self.signArray=temp
