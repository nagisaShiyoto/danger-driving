import cv2
class Img:
    def __init__(self,img):
        self._bgrImg=img
        self._hlsImg=cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
class VideoLoader:
    #open live stream
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("camera isn't available")
    #open video
    def __init__(self,path):
        self.cap=cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise Exception("wron path")
    #move to the next frame
    def nextFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False
        self._img=Img(frame)
        return True
