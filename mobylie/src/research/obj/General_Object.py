#import src.research.obj.Bounding_Box as Bounding_Box
#import src.research.imgDetector as imgeDetector
import mobylie.src.research.imgDetector as imgeDetector
import mobylie.src.research.obj.Bounding_Box as Bounding_Box
import time  # the class for the time management

class Vec:
    # Constructors
    #    def __init__(self): # empty constructor
    #        self.x, self.y = 0, 0

    def __init__(self, x, y):
        self.x, self.y = x, y

    # Class operators
    def __add__(self, other):
        if isinstance(other, Vec):
            self.x += other.x
            self.y += other.y
        else:
            raise TypeError("can't add a type Vec to type" + type(other))

    def __truediv__(self, other):
        if isinstance(other, Vec):
            self.x /= other.x
            self.y /= other.y
        else:
            raise TypeError("can't divide between type Vec and type" + type(other))


class Data:
    # Constructors
    #    def __init__(self): # empty constructor
    #        self.position, self.velocity, self.aceloration, self.positionInPhoto, self.c = Vec(), Vec(), Vec(), Vec(), 0

    def __init__(self, position, velocity, aceloration):
        self.position, self.velocity, self.aceloration, self.positionInPhoto = position, velocity, aceloration, Vec(0,
                                                                                                                    0)


#    def __init__(self, position, velocity, aceloration, positionInPhoto):
#        self.position, self.velocity, self.aceloration, self.positionInPhoto = position, velocity, aceloration, positionInPhoto

class General_Object:
    static_id = 1

    # Constructors
    def __init__(self, bounding_box, name):
        self.bounding_box = bounding_box
        self.name = name
        self.distanceBetweenTwoFrames = Vec(0, 0)
        self.data = Data(Vec(0, 0), Vec(0, 0), Vec(0, 0))
        # the clock a bit funky... returns the time since the Epoch (Jan 1, 1970), but will do
        self.last_check = time.time()  # the time in seconds of the timeStamp from the last update (up to the third decimal point)

        # adding the ID
        self.id = General_Object.static_id
        General_Object.static_id += 1
        ########################test############################
        self.data.position.x = self.id * 2
        self.data.position.y = self.id * 2 + 1
        ########################test############################
        self.distance=imgeDetector.imgDetector.calcDistanceWay1(name,bounding_box)#check for distance

    def make_our_car(self):
        return General_Object(Bounding_Box.Bounding_Box(0, 0, 0, 0), "our Car")

    def calcVec(self, newState, oldState, time):
        # takes vector calc new-las/time
        vel = Vec(0, 0)
        timePassed = float(time - self.last_check)
        vel.x = float(newState.x - oldState.x) / timePassed
        vel.y = float(newState.y - oldState.y) / timePassed
        return vel

    def update(self, oldObj):  # update the last object acorrding to the new data
        newTime = time.time()
        self.name = oldObj.name
        self.id = oldObj.id
        # calc the disnace they did
        self.distanceBetweenTwoFrames.x = self.data.position.x - oldObj.data.position.x
        self.distanceBetweenTwoFrames.y = self.data.position.y - oldObj.data.position.y
        if oldObj.data.position.x != 0 and oldObj.data.position.y != 0:
            vel = oldObj.calcVec(self.data.position, oldObj.data.position, newTime)  # clac vel
            if oldObj.data.velocity.x != 0 and oldObj.data.velocity.y != 0:
                self.data.aceloration = oldObj.calcVec(vel, oldObj.data.velocity, newTime)  # calc acc
            self.data.velocity = vel
        ########################test############################
        print("-------------------------" + self.name + str(self.id) + "-------------------------------")
        print((self.distanceBetweenTwoFrames.x, self.distanceBetweenTwoFrames.y))
        print((self.data.position.x, self.data.position.y))
        print((self.data.velocity.x, self.data.velocity.y))
        print((self.data.aceloration.x, self.data.aceloration.y))
        print("-------------------------" + self.name + str(self.id) + "-------------------------------")
        ########################test############################
        self.last_check = time.time()

    # Getters
    def getBoundingBox(self):
        return self.bounding_box

    def getName(self):
        return self.name

    def getData(self):
        return self.data

    def getLastCheck(self):
        return self.last_check

    def getID(self):
        return self.id

    # Setters
    def setBoundingBox(self, bounding_box):
        self.bounding_box = bounding_box

    def setName(self, name):
        self.name = name

    def setLastCheck(self, last_check):
        self.last_check = last_check

    def setId(self, id):
        self.id = id

    def setData(self, data):
        self.data = data
