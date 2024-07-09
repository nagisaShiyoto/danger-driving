# import src.research.obj.Bounding_Box as Bounding_Box
# import src.research.imgDetector as imgeDetector
import mobylie.src.research.imgDetector as imgeDetector
import mobylie.src.research.obj.Bounding_Box as Bounding_Box
import time  # the class for the time management
import math

class Vec:
    def __init__(self, x, y):
        """
        create the vec
        input: x,y the values of the vectors
        output:none
        """
        self.x, self.y = x, y

    # Class operators
    def __add__(self, other):
        """
        add the values of one vector to other
        input:other-another vector
        output:none
        """
        if isinstance(other, Vec):
            self.x += other.x
            self.y += other.y
        else:
            raise TypeError("can't add a type Vec to type" + type(other))

    def __truediv__(self, other):
        """
        devide one vector with another
        input:other-other vector to divide by
        output:none
        """
        if isinstance(other, Vec):
            self.x /= other.x
            self.y /= other.y
        else:
            raise TypeError("can't divide between type Vec and type" + type(other))


class Data:

    def __init__(self, position, velocity, aceloration):
        """
        create a collection of all the data that can describe obj
        input:position-the dis between our car to the obj
            velocoty-the relitive vel of the obj(reletive to our car)
            aceloration-the accseleration of the obj
        """
        self.position = position
        self.velocity = velocity
        self.aceloration = aceloration
        self.positionInPhoto = Vec(0, 0)


class General_Object:
    static_id = 1

    # Constructors
    def __init__(self, bounding_box, name, imgData):
        """
        create the obj
        input:bounding_box-the place of obj in the img
            name-the type of obj
            imgData-the real lif data of the obj
        output:none
        """
        self.bounding_box = bounding_box
        self.name = name
        self.distanceBetweenTwoFrames = Vec(0, 0)
        self.data = Data(Vec(0, 0), Vec(0, 0), Vec(0, 0))
        # the clock a bit funky... returns the time since the Epoch (Jan 1, 1970), but will do
        self.last_check = time.time()  # the time in seconds of the timeStamp from the last update (up to the third decimal point)

        # adding the ID
        self.id = General_Object.static_id
        General_Object.static_id += 1

        # calc the distance
        self.distance = imgeDetector.imgDetector.calcDistanceWay1(name, bounding_box, imgData)
        # getting the point it checked the distance
        point = Vec(bounding_box.x, (bounding_box.y - (bounding_box.length / 2)))

        if (name != "our_car"):
            self.data.position.x, self.data.position.y = self.get_X_Y_distance(self.distance, point)

    def get_X_Y_distance(self, distance_from_point, point):
        """
        separate the distance to x and y cordinate
        input:distance_from_point-real lif dis
            point-the place of the point in the img
        output:the two distances(x and y)
        """
        rad_degree = math.atan(point.y / point.x)
        x_distance = distance_from_point * math.cos(rad_degree)
        y_distance = distance_from_point * math.sin(rad_degree)
        return x_distance, y_distance

    def make_our_car(self):
        """
        creates our car with 0 as values and our car as name
        input:none
        output:none
        """
        return General_Object(Bounding_Box.Bounding_Box(0, 0, 0, 0), "our Car")

    def calc_vec(self, newState, oldState, time):
        """
        calc the differance in values divided by the time
        input:newState,oldState-the states(values) to compare
            time-the time passed in secondes
        output:the result(as a vector)

        """
        # takes vector calc new-las/time
        vel = Vec(0, 0)
        timePassed = float(time - self.last_check)
        vel.x = float(newState.x - oldState.x) / timePassed
        vel.y = float(newState.y - oldState.y) / timePassed
        return vel

    def print_object_data(self):
        """
        print the object on data
        input:none
        output:none
        """
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + self.name + str(self.id) + "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print((self.distanceBetweenTwoFrames.x, self.distanceBetweenTwoFrames.y))
        print((self.data.position.x, self.data.position.y))
        print((self.data.velocity.x, self.data.velocity.y))
        print((self.data.aceloration.x, self.data.aceloration.y))
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + self.name + str(self.id) + "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    def update(self, oldObj, printData):
        """
        update the last object according to the new data
        input:oldObj-the obj to compare
        output:none
        """
        newTime = time.time()
        self.name = oldObj.name
        self.id = oldObj.id
        # calc the distance they did
        self.distanceBetweenTwoFrames.x = self.data.position.x - oldObj.data.position.x
        self.distanceBetweenTwoFrames.y = self.data.position.y - oldObj.data.position.y
        if oldObj.data.position.x != 0 and oldObj.data.position.y != 0:
            # calc vel
            vel = oldObj.calc_vec(self.data.position, oldObj.data.position, newTime)
            if oldObj.data.velocity.x != 0 and oldObj.data.velocity.y != 0:
                # calc acc
                self.data.aceloration = oldObj.calc_vec(vel, oldObj.data.velocity, newTime)
            self.data.velocity = vel

        if printData:
            self.print_object_data()

        # save the time
        self.last_check = time.time()
