import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
#create a gussion blur kernel (to surpress noise)
def gaussion_kernal(size,sigma=1):
    size=int(size)
    x, y= np.mgrid[-size:size+1,-size:size+1]
    normal=1/(2.0*np.pi*sigma**2)
    #we don't need the mean because we know it's 0
    g=np.exp(-((x**2+y**2)/(2.0*sigma**2)))*normal
    return g

def sobal_filter(img):
    Kx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]],np.float32)
    Ky=np.array([[1,2,1],[0,0,0],[-1,-2,-1]],np.float32)

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

def threshold(img,lowThresholdRatio=0.05,highThresholdRatio=0.09):
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
def main():
    img=cv2.imread("../videos/4.jpg")
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernal=gaussion_kernal(size=6,sigma=3)
    blurred_img=cv2.filter2D(img,-1,kernal)
    line_Image,slope=sobal_filter(blurred_img)
    maxed_img=non_max_suppression(line_Image,slope)
    thresholdImg,weak,strong=threshold(maxed_img)

    plt.imshow(thresholdImg, cmap="gray")
    plt.title("hi ma k")
    plt.axis("off")
    plt.show()
    plt.imshow(maxed_img, cmap="gray")
    plt.title("hi ma")
    plt.axis("off")
    plt.show()
    plt.imshow(line_Image, cmap="gray")
    plt.title("hi m")
    plt.axis("off")
    plt.show()
    cv2.imshow("h",img)
    cv2.imshow("hi",blurred_img)

    if cv2.waitKey(100000) == ord('q'):
        breakpoint()
if __name__ == '__main__':
    main()