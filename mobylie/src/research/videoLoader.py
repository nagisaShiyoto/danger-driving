import cv2
import numpy
import json



class Img:
    def __init__(self, img):
        """
        create images to use
        input:img-rgb img
        output: none
        """
        self._bgrImg = img
        self._hlsImg = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

class VideoLoader:
    # open live stream

    def __init__(self):
        """
        set the setting to get realtime images
        input:none
        output:none
        """
        self.cap = cv2.VideoCapture(0)
        self.config_data = self.read_config()
        if not self.cap.isOpened():
            raise Exception("camera isn't available")

    # open video
    def __init__(self, path):
        """
        set the setting to get the images from a video
        input:path-the path to the vid
        output:none
        """
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise Exception("wrong path")
        self.config_data = self.read_config()
        self._img=0

    @staticmethod
    def read_config():
        """
        read the config file to get the setting of the project
        input:none
        output: the config data
        """
        # Opening JSON file
        f = open('../../../config.json')

        # reading the data from the JSON object
        config_data = json.load(f)



        # Closing file
        f.close()
        return config_data

    # move to the next frame
    def nextFrame(self):
        """
        get the next avilable frame
        and adjust to our wanted size
        input:none
        output:true-has a frame,false-coudnt get any frame
        """
        ret, frame = self.cap.read()
        if not ret:
            return False
        self._prevImg=self._img
        self._img = Img(cv2.resize(frame,
                                   (self.config_data["calculating info"]["image width"],
                                    self.config_data["calculating info"]["image height"]),
                                   interpolation=cv2.INTER_AREA))
        return True

    def showObjects(self,objects,color,thikness=1):
        """
        show the dettected objects on an img
        input:objects-array of dettected objects
            color-the color of the text and bounding box
            thikness- the thikness of the text and bounding box
        """
        for object in objects:#run on all the objects

            #gets and adjust the needed points of the bounding box:
            top_left = object.bounding_box.getTopLeftPoint(object.bounding_box.x, object.bounding_box.y, object.bounding_box.width,
                                                        object.bounding_box.length)
            bottom_right = object.bounding_box.getBottomRightPoint(object.bounding_box.x, object.bounding_box.y,
                                                                object.bounding_box.width, object.bounding_box.length)
            intTopLeft = (int(top_left[0]), int(top_left[1]))  # parse from float to int
            intBottomRight = (int(bottom_right[0]), int(bottom_right[1]))  # parse from float to int
            #color the bounding box
            cv2.rectangle(self._img._bgrImg, intTopLeft, intBottomRight, color, thikness)


            #the text to show
            text = (str(int(object.data.position.x)) + " " \
                    + str(int(object.data.position.y)) + " " \
                    + str(int(object.distance))
                    )

            #text settings
            text_position = (intTopLeft[0], intBottomRight[1] - 10)
            font_face = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            text_color = color
            text_thickness = thikness

            #write the text
            cv2.putText(self._img._bgrImg, text,
                        text_position, font_face,
                        font_scale, text_color, text_thickness)