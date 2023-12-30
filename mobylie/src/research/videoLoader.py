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
    def showSegmentation(self,carVec):

        pic=self._img._bgrImg
        rowCounter=0
        colCounter=0
        self.segmentation(carVec)
        print(self.answers_array)
        while rowCounter < pic.shape[0]:
            colCounter=0
            while colCounter<pic.shape[1]:
                if(self.answers_array[rowCounter, colCounter]==1):
                    pic[rowCounter, colCounter]=(255,255,255)
                else:
                    pic[rowCounter, colCounter]=(0,0,0)
                colCounter+=1
            rowCounter+=1
        return pic
    def segmentation(self, carVec):
        points_of_interest = self.find_points_of_interest(carVec)
        (height,length,place)= self._img._hlsImg.shape
        self.check_array = numpy.zeros((height,length),dtype=int)
        self.answers_array = numpy.zeros((height,length),dtype=int)

        # points_of_interest is an array of tuples representing points
        for point in points_of_interest:
            self.check_pixel(point[0], point[1],(-1,-1,-1),True)



    def check_pixel(self, i, j_Float, last_pixel_BGR,firstPixel):
        j = int(j_Float)
        if i > 0 and j > 0 \
                and (i < self._img._hlsImg.shape[0]) \
                and (j < self._img._hlsImg.shape[1]):
            if self.check_array[i, j] == 0: # if it wan't checked already
                self.check_array[i,j] = 1

                HLS_values = self._img._hlsImg[i,j]

                # determining the hsl threshold
                s_threshold = 10
                l_threshold = 25
                print(l_threshold)
                #checking if the hsl is matching
                if((HLS_values[2] < s_threshold) & HLS_values[1] < l_threshold):
                    #at this point the pixel itself is clear. we need to check it's neighbors
                    #if it's the first pixel in the chain we will send the RGB tuple as -1,-1,-1
                    if firstPixel:
                        self.answers_array[i][j] = 1
                        # checking the same thing for all of the adjacent pixels
                        self.check_pixel(i - 1, j, (self._img._bgrImg[i,j]),False)
                        self.check_pixel(i + 1, j, (self._img._bgrImg[i,j]),False)
                        self.check_pixel(i, j - 1, (self._img._bgrImg[i,j]),False)
                        self.check_pixel(i, j + 1, (self._img._bgrImg[i,j]),False)

                    #otherwise
                    else:

                        b_offset = abs((self._img._bgrImg[i,j])[0] - last_pixel_BGR[0])
                        g_offset = abs((self._img._bgrImg[i,j])[1] - last_pixel_BGR[1])
                        r_offset = abs((self._img._bgrImg[i,j])[2] - last_pixel_BGR[2])
                        print(b_offset,r_offset,g_offset)
                        if(b_offset < 10 and g_offset < 10 and r_offset < 10):
                            self.answers_array[i, j] = 1
                            # checking the same thing for all of the adjacent pixels
                            self.check_pixel(i + 1, j, (self._img._bgrImg[i,j]),False)
                            self.check_pixel(i - 1, j, (self._img._bgrImg[i,j]),False)
                            self.check_pixel(i, j - 1, (self._img._bgrImg[i,j]),False)
                            self.check_pixel(i, j + 1, (self._img._bgrImg[i,j]),False)

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
