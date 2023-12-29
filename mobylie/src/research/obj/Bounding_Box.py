class Bounding_Box:  # a class that represents a bounding box

    # Constructors
    def __init__(self):  # an empty constructors
        self.x = 0
        self.y = 0
        self.width = 0
        self.length = 0

    def __init__(self, x, y, width, length):
        # we get as a defult the middle point. here we are transforming it to the top left point why though?
        self.x = x
        self.y = y
        self.width = width
        self.length = length

    # Methods
    def calculateIUO(self, other):
        if isinstance(other, Bounding_Box):
            xy1 = self.getTopLeftPoint(self.x, self.y, self.width, self.length)
            xy2 = self.getTopLeftPoint(other.x, other.y, other.width, other.length)
            # calculateing our and other areas
            self_area = self.width * self.length
            other_area = other.width * other.length

            # finding the intersection box coordinates
            x_left = max(xy1[0], xy2[0])
            y_top = min(xy1[1], xy2[1])
            x_right = min((xy1[0] + self.width), (xy2[0] + other.width))
            y_bottom = max((xy1[1] - self.length), (xy2[1] - other.length))

            # calculating the intersection box area
            intersection_area = max(0, abs(x_left - x_right)) * max(0, abs(y_top - y_bottom))

            # calculating the IUO
            union_area = self_area + other_area - intersection_area
            iuo = intersection_area / union_area

            return iuo

        else:
            raise TypeError("can't calculate IUO between type Bounding_Box and type: " + type(other))

    @staticmethod
    def getTopLeftPoint(x, y, width, length):
        x -= (width / 2)
        y += (length / 2)
        return (x, y)

    @staticmethod
    def getBottomRightPoint(x, y, width, length):
        x += (width / 2)
        y -= (length / 2)
        return (x, y)

    # Setters
    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setWidth(self, width):
        self.width = width

    def setLength(self, length):
        self.length = length

    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getLength(self):
        return self.length
