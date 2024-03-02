import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
from PIL import Image

from mobylie.src.research import videoLoader


def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray


#create a gussion blur kernel (to surpress noise)
def gaussion_kernal(size,sigma=1):
    size=int(size)
    x, y= np.mgrid[-size:size+1,-size:size+1]
    normal=1/(2.0*np.pi*sigma**2)
    #we don't need the mean because we know it's 0
    g=np.exp(-((x**2+y**2)/(2.0*sigma**2)))*normal
    return g

def sobal_filter(img):

    Kx=np.array([[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]],np.float32)
    Ky=np.array([[1,2,1],
                        [0,0,0],
                    [-1,-2,-1]],np.float32)

    #makes the convolation for straight line dettection
    Ix=ndimage.convolve(img,Kx)
    #makes the convoloation for horazontol line dettection
    Iy=ndimage.convolve(img,Ky)

    #calculate the importance of every pixel to the line
    G=np.hypot(Ix,Iy)
    G=G/(G.max()*255)

    theta=np.arctan2(Ix,Iy)

    return G,theta

#make line less wide
def non_max_suppression(img,D):
    M, N = img.shape
    #why G is float?
    Z = np.zeros((M,N),dtype=np.float32)
    #turnes the degree to radian
    angle = D *180./np.pi
    angle[angle<0]+=180
    for i in range(1,M-1):
        for j in range(1,N-1):
            try:

                q=255
                r=255

                #gets the same diraction pixels
                #there is 4 options
                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = img[i, j + 1]
                    r = img[i, j - 1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = img[i + 1, j - 1]
                    r = img[i - 1, j + 1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = img[i + 1, j]
                    r = img[i - 1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = img[i - 1, j - 1]
                    r = img[i + 1, j + 1]

                #check who is more intance and put it accordingly
                if (img[i, j] >= q) and (img[i, j] >= r):
                    Z[i, j] = img[i, j]
                else:
                    Z[i, j] = 0
            except IndexError as e:
                pass
    return Z

def threshold(img,lowThresholdRatio=0.05,highThresholdRatio=0.15):
    highThreshold=img.max()*highThresholdRatio
    lowThreshold=highThreshold*lowThresholdRatio

    M,N=img.shape
    res = np.zeros((M,N),dtype=np.int32)#probably need float

    weak=np.int32(25)
    strong=np.int32(255)

    #catogerize every pixel acording to the thresholds
    strong_i,strong_j=np.where(img>highThreshold)#mybe need to do =>
    zeros_i,zeros_j=np.where(img<lowThreshold)
    weak_i,weak_j=np.where((img<=highThreshold)&(img>=lowThreshold))

    #unite the pixels
    res[strong_i,strong_j]=strong
    res[weak_i,weak_j]=weak

    return (res,weak,strong)
#make weak line strong if it has strong pixel surronding it
#otherwise turn it to 0
def hysteresis(img,weak,strong=255):
    M, N = img.shape
    for i in range(1,M-1):
        for j in range (1,N-1):
            if(img[i,j] == weak):
                try:
                    if (
                            (img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)
                    ):
                        img[i, j] = strong
                    else:
                        img[i, j]=0
                except IndexError as e:
                    pass
    return img

def main():
    img1=cv2.imread("../videos/5.png")
    img=rgb2gray(img1)
    kernal=gaussion_kernal(size=5,sigma=2.5)
    blurred_img=cv2.filter2D(img,-1,kernal)
    line_Image,slope=sobal_filter(blurred_img)
    maxed_img=non_max_suppression(line_Image,slope)
    thresholdImg,weak,strong=threshold(maxed_img)
    segmentatedImg=hysteresis(thresholdImg,weak,strong)
#//////////////////sobal-segmentation///////////////////////////
    segmentatedImg=np.array(segmentatedImg,np.uint8)
    find_reqtangles(segmentatedImg,img1)


    plt.imshow(segmentatedImg, cmap="gray")
    plt.title("hi ma kore ahi?")
    plt.axis("off")
    plt.show()



    if cv2.waitKey(100000) == ord('q'):
        breakpoint()











def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
def gaussian_blur(img, kernel_size = 5):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 2)
def canny(img, low_threshold = 50, high_threshold = 150):
    return cv2.Canny(img, low_threshold, high_threshold)


def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, pts=[vertices],color= ignore_mask_color)


    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 255, 255], thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines_basic(img, rho=2, theta=np.pi / 180, threshold=25, min_line_len=50, max_line_gap=10):
    """
    `img` should be the output of a Canny transform.
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)


    #return lines




    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #print(lines.size)
    draw_lines(line_img, lines)
    return line_img




def find_reqtangles(img,img1):
    detected=""
    #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # Approximate contours with polygons using RANSAC
    for con in cnts:
        approx=cv2.approxPolyDP(con, 0.01 * cv2.arcLength(con, True), False)

        if (4 <= len(approx) <= 12 and cv2.contourArea(con)>0.5):
            x, y, w, h = cv2.boundingRect(approx)
            if h>10 and w<150:
                #cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
                detected += ("[" + str(x+(w/2)) + ", " +
                           str(y+(h/2)) + ", " +
                           str(w) + ", " +
                           str(h) + "],line\n")
    return detected


def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

def select_white_yellow(image):
    converted = convert_hls(image)
    # white color mask
    lower = np.uint8([  0, 200,   0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(converted, lower, upper)
    # yellow color mask
    lower = np.uint8([ 10,   0, 100])
    upper = np.uint8([ 40, 255, 255])
    yellow_mask = cv2.inRange(converted, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    return cv2.bitwise_and(image, image, mask = mask)


def find_squre(lines,img):
    for line in lines:
        for line2 in lines:
            x1, y1, x2, y2 = line[0]
            x3, y3, x4, y4 = line2[0]
            #if it touch it
            if(x1==x3 or x1==x4 or x1==x2):
                continue
            if(abs(x2-x4)>0.5 and abs(x1-x3)>0.5):
                continue
            xd1 = x1 - x2
            yd2 = y1 - y2
            xd3 = x3 - x4
            yd4 = y3 - y4
            #if it has the same float
            if((yd2/xd1)==(yd4/xd3)):
                cv2.rectangle(img,(x1,y1),(x4,y4),(255,0,0),2)
    return img,img
            #only 1 iteration
            #for x1,y1,x2,y2 in line:
            #    for x3,y3,x4,y4 in line2:
            #        if(x1==x2 and )






def dettect(img):
    whiteYelloImg=select_white_yellow(img)
    grayImg=grayscale(whiteYelloImg)
    blurrImg=gaussian_blur(grayImg)
    cannyImg=canny(blurrImg)
    pointsPolly = np.array([[0, 270],
                            [0, 360],
                            [570, 400],
                            [350, 230],
                            [270,230]], dtype=np.int32)
    spaceImg=region_of_interest(cannyImg,pointsPolly)
    #lineImg=hough_lines_basic(spaceImg)
    return find_reqtangles(spaceImg, img)

    cv2.imshow("img",img)
    cv2.imshow("gray",grayImg)
    cv2.imshow("blurr",blurrImg)
    cv2.imwrite("canny.png",cannyImg)
    cv2.imshow("ragion",spaceImg)
    cv2.imshow("lines",lineImg)
    cv2.waitKey(100)
    cv2.destroyAllWindows()
    #return find_squre(lineImg, img)
    return find_reqtangles(spaceImg, img)

import imgDetector
if __name__ == '__main__':
    loader = videoLoader.VideoLoader("../videos/highway1.mp4")
    #loader.nextFrame()
    dettector = imgDetector.imgDetector()
    while loader.nextFrame():
        txt=(dettect(loader._img._bgrImg))
        dettector.updateSign(txt)
        for car in dettector.signArray:
            top_left = car.bounding_box.getTopLeftPoint(car.bounding_box.x, car.bounding_box.y, car.bounding_box.width,
                                                        car.bounding_box.length)
            bottom_right = car.bounding_box.getBottomRightPoint(car.bounding_box.x, car.bounding_box.y,
                                                                car.bounding_box.width, car.bounding_box.length)
            intTopLeft = (int(top_left[0]), int(top_left[1]))  # parse from float to int
            intBottomRight = (int(bottom_right[0]), int(bottom_right[1]))  # parse from float to int
            cv2.rectangle(loader._img._bgrImg, intTopLeft, intBottomRight, (255, 0, 0), 1)
        cv2.imshow("Asd",loader._img._bgrImg)
        if cv2.waitKey(100) == ord('q'):
            break
