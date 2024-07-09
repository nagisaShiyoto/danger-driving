import numpy as np
import cv2
def grayscale(img):
    """
    transfer the img to grayscale
    input:img-rbg img
    output:gray_scale img
    """
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size = 5):
    """
    makes the img more blurred to avoid oversensitive detection
    input:img-grayScale img
        kernal_size-how much blurred the image is, only nonevan num
    output: blurred img
    """
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 2)
def canny(img, low_threshold = 50, high_threshold = 150):
    """
    use canny operation to detect lines
    input:img-the blurred img
            low_threshold-minimal amount of certainty to count a weak line
             high_threshold-minimal amount of certainty to count a strong line
    output:img where there is only lines
    """
    return cv2.Canny(img, low_threshold, high_threshold)


def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    input:img- the img with the line
            vertics- array of points of the area you interested in
    output: img where only the line in the region are shown
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

def find_rectangles(img,minimal_erea=0.5,minimal_sides=4,max_sides=12,minimal_hight=10,maximal_width=150):
    """
    finds the lines(rectangles in the img)
    input: img-img where you there are only lines
            minimal_area=,minimal_sides,max_sides-to ensure it is a rectangles
            minimal_height,maximal_width- to ensure the rectangles are the wanted lines
    output: string of all the rectangles found
    """
    detected=""
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # Approximate contours with polygons using RANSAC
    for con in cnts:
        approx=cv2.approxPolyDP(con, 0.01 * cv2.arcLength(con, True), False)
        #4<amount of sides<12 because of noisess
        if (minimal_sides <= len(approx) <= max_sides and cv2.contourArea(con)>minimal_erea):
            x, y, w, h = cv2.boundingRect(approx)
            if h > minimal_hight and w < maximal_width:
                detected += ("[" + str(x+(w/2)) + ", " +
                           str(y+(h/2)) + ", " +
                           str(w) + ", " +
                           str(h) + "],line\n")
    return detected

def convert_hls(image):
    """
    convert the rgb format to hls
    input:image-rgb img
    output: hsl img
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

def select_white_yellow(image):
    """
    choose to show only the white\yellow pixels
    input:image-hsl img
    output: hsl image where everything black except white\yellow
    """
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

def dettect(img):
    """
    detect all the lines in rgb img
    input:img-rgb img
    output: string of all the lines
    """
    whiteYelloImg=select_white_yellow(img)
    grayImg=grayscale(whiteYelloImg)
    blurrImg=gaussian_blur(grayImg)
    cannyImg=canny(blurrImg)
    pointsPolly = np.array([[10, 270],
                            [10, 340],
                            [550, 390],
                            [315, 220],
                            [240,240]], dtype=np.int32)
    spaceImg=region_of_interest(cannyImg,pointsPolly)
    return find_rectangles(spaceImg)
