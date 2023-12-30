import cv2
import numpy

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
        self._img = Img(frame)
        return True

    def segmentation(self, carVec):
        points_of_interest = self.find_points_of_interest(carVec)

        self.check_array = numpy.zeros(self._hlsImg.shape()[0], self._hlsImg.shape()[1])
        self.answers_array = numpy.zeros(self._hlsImg.shape()[0], self._hlsImg.shape()[1])

        # points_of_interest is an array of tuples representing points
        for point in points_of_interest:
            self.check_pixel(point[1], point[2], (-1, -1, -1))



    def check_pixel(self, i, j, last_pixel_BGR):
        if(i > 0 & j > 0 & (i < self._hlsImg.shape()[0]) & (j < self._hlsImg.shape()[1])):
            if self.check_array[i][j] == 0: # if it wan't checked already
                self.check_array[i][j] = 1

                HSL_values = self._hlsImg[i][j]

                # determining the hsl threshold
                s_threshold = 10
                l_threshold = 40 - HSL_values[1] * 2

                #checking if the hsl is matching
                if((HSL_values[1] < s_threshold) & HSL_values[2] < l_threshold):
                    #at this point the pixel itself is clear. we need to check it's neighbors

                    #if it's the first pixel in the chain we will send the RGB tuple as -1,-1,-1
                    if ((last_pixel_BGR[0] == -1)&(last_pixel_BGR[1] == -1)&(last_pixel_BGR[2] == -1)):
                        self.answers_array[i][j] = 1

                        # checking the same thing for all of the adjacent pixels
                        self.check_pixel(i - 1, j, (self._bgrImg[i][j]))
                        self.check_pixel(i + 1, j, (self._bgrImg[i][j]))
                        self.check_pixel(i, j - 1, (self._bgrImg[i][j]))
                        self.check_pixel(i, j + 1, (self._bgrImg[i][j]))

                    #otherwise
                    else:
                        b_offset = abs((self._bgrImg[i][j])[0] - last_pixel_BGR[0])
                        g_offset = abs((self._bgrImg[i][j])[1] - last_pixel_BGR[1])
                        r_offset = abs((self._bgrImg[i][j])[2] - last_pixel_BGR[2])

                        if(b_offset < 10 & g_offset < 10 & r_offset < 10):
                            self.answers_array[i][j] = 1

                            # checking the same thing for all of the adjacent pixels
                            self.check_pixel(i - 1, j, (self._bgrImg[i][j]))
                            self.check_pixel(i + 1, j, (self._bgrImg[i][j]))
                            self.check_pixel(i, j - 1, (self._bgrImg[i][j]))
                            self.check_pixel(i, j + 1, (self._bgrImg[i][j]))

    def find_points_of_interest(self, carVec):
        points_of_interest = []

        for car in carVec:

            i = 0
            while i < car.bounding_box.width:
                y = car.bounding_box.y - (car.bounding_box.hight / 2)
                x = car.bounding_box.x + i
                i += 1

                points_of_interest.append((x, y))