import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

"""
to visualize the gruph for twsting
input:x,y points,b-the slpoe and the b of the graph
output:none
"""
def plot_regression_line(x, y, b):
  # plotting the actual points as scatter plot
  plt.scatter(x, y, color = "m",
        marker = "+", s = 30)

  # predicted response vector
  y_pred = b[0] + b[1]*x

  # plotting the regression line
  plt.plot(list(x), y_pred, color = "g")

  # putting labels
  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()



class cca_model:
    AMOUNT_OF_X_VARS=8
    """create the class, calc weight, create prediction"""
    def __init__(self,data):

        self.weighTracker={}
        Tracker,allData=cca_model.dictToArrays(data)#create an array from a dict
        self.weights=cca_model.calc_weights(allData[:self.AMOUNT_OF_X_VARS],np.tile(allData[self.AMOUNT_OF_X_VARS:],(self.AMOUNT_OF_X_VARS,1)))
        for key,value in Tracker.items():
            #make a dict with name and weight
            self.weighTracker[key]=self.weights[value]
        points=cca_model.calcLinarPoint(allData,self.weights)#create the linear point from data
        self.m,self.b,r,p,std_err=stats.linregress(points[0],points[1])#calc the regrassion
        #plot_regression_line(points[0],points[1],(self.b,self.m))#testing the model
    """
    getting from dettector the values for the prediction
    input:dettector-the one with all the values
        Y_values-say if we want the y values(1) or the x values(0)
    output: the data we need for prediction
    """
    @staticmethod
    def getValues(dettector,Y_values):
        angle=0
        sumVel=[0,0]
        for car in dettector.carArray:
            sumVel[0]+=car.data.velocity.x
            sumVel[1]+=car.data.velocity.y
        if( dettector.ourCar.data.position.y!=0):
            angle=math.tan(dettector.ourCar.data.position.x/dettector.ourCar.data.position.y)
        return (angle,
         dettector.ourCar.data.velocity.x,
         dettector.ourCar.data.aceloration.x,
         len(dettector.carArray),
         sumVel[Y_values]/len(dettector.carArray),
         0,0,0)
    """
    make a correlation based prediction
    input:the state of the system
    output: the future state 
    """
    def predict(self,input):
        #create the state by adding the weighted vars
        state=np.sum(input*self.weights[:len(input)])
        #y        =    b +   m  *   x
        prediction=self.b+self.m*state
        return prediction/self.weights[8]

    """
    create an array from dictonary
    input: dictinary with names as key and arrays of data as values
    output:tracker-a dictinary with name and his place in the array
            data-array of all the data array
    """
    @staticmethod
    def dictToArrays(dictinary_data):
        data=[]
        tracker={}
        for key,value in dictinary_data.items():
            data.append(value)
            tracker[key]=len(data)-1
        return tracker,data

    """
    after the creation of the waights we need to create the value of that weights
    input:allData-array of arrays with all the needed data
                    weight- the weight we need to put on every array
    output: the point on the gruph(input-X,resualt-Y)
    """
    @staticmethod
    def calcLinarPoint(allData,weights):
        weighted_points=[]
        for idx,wight in enumerate(weights):
            weighted_points.append(np.dot(wight,allData[idx]))
        #adding it to one row
        input=weighted_points[0]+weighted_points[1]+\
              weighted_points[2]+weighted_points[3]+\
              weighted_points[4]+weighted_points[5]+\
              weighted_points[6]+weighted_points[7]
        result=weighted_points[8]
        return input,result

    """
    calc the eigenVector and eigenValue of the multypication of 4 matrixes
    input:the matrixes by order
    output:eigenValue-good to have,
        eigenVector-from here we can get the weights,
        wanted_value_vector-the col of the weights(from the eigenValue matrix)
    """
    @staticmethod
    def getEigenVector(first,second,third,last):
        #nultyplying the matrixes,the order is important
        Rx = np.matmul(np.matmul(np.matmul(first, second), third),last)
        eigenValue,eigenVector=np.linalg.eig(Rx)
        #check which weights has the best correlation
        wanted_value_vector=np.argmax(np.sqrt(eigenValue))
        return eigenValue,eigenVector,wanted_value_vector

    """
    calculating the weights of the CCA model for the prediction
    input:input_data-the data we get in the prediction time
        output_data-the data we want to infer,
        both of these data we get now for the prediction
    output:array of all the weights
    """
    @staticmethod
    def calc_weights(input_data,output_data):
        #calculating the covariance matrix
        cov=np.cov(input_data,output_data)
        Rxx=cov[:-len(input_data),:-len(output_data)]#cov(x,x)
        Ryy=cov[-len(input_data):,-len(output_data):]#cov(y,y)
        Ryx=cov[-len(input_data):,:-len(output_data)]#cov(y,x)
        Rxy=Ryx.transpose()

        #getting the eigenVector(the weights)
        input_values,intput_weight,input_wanted_value=\
            cca_model.getEigenVector(np.linalg.pinv(Rxx),
                                     Rxy,np.linalg.pinv(Ryy),Ryx)

        output_values,output_weight,output_wanted_value=\
            cca_model.getEigenVector( np.linalg.pinv(Ryy),
                                      Ryx,np.linalg.pinv(Rxx), Rxy)

        #making the input_wieght and output_weight on array  and getting only the weight we need
        return np.append(intput_weight[:,input_wanted_value],(output_weight[0,output_wanted_value]))
