import cv2
import numpy

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 420


class Img:
    def __init__(self, img):
        self._bgrImg = img
        self._hlsImg = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)


class VideoLoader:
    # open live stream
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("camera isn't available")

    # open video
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise Exception("wrong path")


    # move to the next frame
    def nextFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False
        self._img = Img(cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation=cv2.INTER_AREA))
        return True

    def showSegmentation(self, carVec):

        pic = self._img._bgrImg
        rowCounter = 0
        colCounter = 0
        self.segmentationloop(carVec)
        print(self.answers_array)
        while rowCounter < pic.shape[0]:
            colCounter = 0
            while colCounter < pic.shape[1]:
                number = self.answers_array[rowCounter, colCounter] * 50
                pic[rowCounter, colCounter] = (number, number, number)
                colCounter += 1
            rowCounter += 1
        return pic

    def segmentationloop(self, carVec):
        boxSize = 3
        placeCounter = 1
        (height, length, place) = self._img._hlsImg.shape
        self.answers_array = numpy.zeros((height, length), dtype=int)
        for rowIndex, row in enumerate(self._img._bgrImg):
            for colIndex, col in enumerate(row):
                if (not self.check_seruonding_pixels(placeCounter, boxSize,
                                                     (rowIndex - 1, colIndex - 1), (rowIndex, colIndex))):
                    placeCounter += 1

    def check_seruonding_pixels(self, placeCounter, boxSize, startPlace, pixel):
        """run on a box of pixels, compare each pixel to a certain pixel and categorize them
        output: true-change the placeCounter
                false-didnt change"""
        highestOffsetAvg = 75
        lowestOffset = highestOffsetAvg
        col = startPlace[1]
        row = startPlace[0]
        changedPlaceCounter = False
        matchingPoint = [(pixel[0], pixel[1])]
        # run on a boxSize by boxSixe box in pixels
        while (row < boxSize + startPlace[0]):
            col = startPlace[1]
            while (col < boxSize + startPlace[1]):
                # check thair offset
                offset = self.check_like_pixel(row, col, self._img._bgrImg[pixel[0], pixel[1]])
                if (offset <= highestOffsetAvg and (row != pixel[0] or col != pixel[1])):
                    if (self.answers_array[row, col] == 0):
                        # adds him to the pixel's group
                        self.answers_array[row, col] = placeCounter
                        matchingPoint.append((row, col))
                    elif lowestOffset > offset:
                        # find the most similiur pixel
                        placeCounter = self.answers_array[row, col]
                        changedPlaceCounter = True
                    # else:
                    #    matchingPoint.append((row,col))
                col += 1
            row += 1
        for place in matchingPoint:
            # put all the pixels in their places
            self.answers_array[place[0], place[1]] = placeCounter
        return changedPlaceCounter

    def check_like_pixel(self, row, col, pixel):
        highNum = 100000
        depth = 3  # the amount of vars every pixel represented by
        if row >= 0 and col >= 0 \
                and (row < self._img._bgrImg.shape[0]) \
                and (col < self._img._bgrImg.shape[1]):
            b_offset = abs((self._img._bgrImg[row, col])[0] - pixel[0])
            g_offset = abs((self._img._bgrImg[row, col])[1] - pixel[1])
            r_offset = abs((self._img._bgrImg[row, col])[2] - pixel[2])
            return ((b_offset + r_offset + g_offset) / depth)
        return highNum

    def segmentation(self, carVec):

        points_of_interest = self.find_points_of_interest(carVec)
        (height, length, place) = self._img._hlsImg.shape
        self.check_array = numpy.zeros((height, length), dtype=int)
        self.answers_array = numpy.zeros((height, length), dtype=int)

        # points_of_interest is an array of tuples representing points
        for point in points_of_interest:
            self.check_pixel(point[0], point[1], (-1, -1, -1), True)

    def check_pixel(self, i, j_Float, last_pixel_BGR, firstPixel):
        j = int(j_Float)
        if i > 0 and j > 0 \
                and (i < self._img._hlsImg.shape[0]) \
                and (j < self._img._hlsImg.shape[1]):
            if self.check_array[i, j] == 0:  # if it wan't checked already
                self.check_array[i, j] = 1

                HLS_values = self._img._hlsImg[i, j]

                # determining the hsl threshold
                s_threshold = 50
                l_threshold = 100
                offset = 10000000
                # checking if the hsl is matching
                if ((HLS_values[2] < s_threshold) and HLS_values[1] < l_threshold):
                    # at this point the pixel itself is clear. we need to check it's neighbors
                    # if it's the first pixel in the chain we will send the RGB tuple as -1,-1,-1
                    if firstPixel:
                        self.answers_array[i][j] = 1
                        # checking the same thing for all of the adjacent pixels
                        self.check_pixel(i - 1, j, (self._img._bgrImg[i, j]), False)
                        self.check_pixel(i + 1, j, (self._img._bgrImg[i, j]), False)
                        self.check_pixel(i, j - 1, (self._img._bgrImg[i, j]), False)
                        self.check_pixel(i, j + 1, (self._img._bgrImg[i, j]), False)

                    # otherwise
                    else:
                        b_offset = abs((self._img._bgrImg[i, j])[0] - last_pixel_BGR[0])
                        g_offset = abs((self._img._bgrImg[i, j])[1] - last_pixel_BGR[1])
                        r_offset = abs((self._img._bgrImg[i, j])[2] - last_pixel_BGR[2])
                        print(b_offset, r_offset, g_offset)
                        if (b_offset < offset and g_offset < offset and r_offset < offset):
                            self.answers_array[i, j] = 1
                            # checking the same thing for all of the adjacent pixels
                            self.check_pixel(i + 1, j, (self._img._bgrImg[i, j]), False)
                            self.check_pixel(i - 1, j, (self._img._bgrImg[i, j]), False)
                            self.check_pixel(i, j - 1, (self._img._bgrImg[i, j]), False)
                            self.check_pixel(i, j + 1, (self._img._bgrImg[i, j]), False)

    def find_points_of_interest(self, carVec):
        points_of_interest = []

        for car in carVec:

            i = 0
            while i < car.bounding_box.width:
                y = car.bounding_box.y - (car.bounding_box.length / 2)
                x = car.bounding_box.x + i
                i += 1
                points_of_interest.append((x, y))
        return points_of_interest
