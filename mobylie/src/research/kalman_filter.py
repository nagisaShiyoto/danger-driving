import numpy as np
import numpy.linalg


class KalmanFilter:
    def __init__(self, F, Q, H, X, P, R):
        """
        create the first time matrices and vectors
        input: F-the physical transformation matrix
                Q-the error place of the F matrix
                H-the matrix to adjust the F
                X-the first state of our car
                P-the error matrix
                R-the error place of the prediction
        output:none
        """
        self.F = np.array(F)
        self.Q = np.array(Q)
        self.Ft = np.transpose(F)
        self.H = np.array(H)
        self.Ht = np.transpose(H)
        self.X = np.array(X)
        self.P = np.array(P)
        self.R = np.array(R)
        self.K = []

    def predictG(self):
        """
        do the first prediction phase(of prediction)
        input:none
        output:none
        """
        self.X = self.F.dot(self.X)
        self.P = self.F.dot(self.P).dot(self.Ft) + self.Q

    def updateG(self, Z):
        """
        do the update phase(of the prediction)
        input:Z-the result of the CCA model
        output: none
        """
        self.K = self.P.dot(self.Ht).dot(numpy.linalg.inv((self.H.dot(self.P.dot(self.Ht)) + self.R)))
        self.X = self.X +self.K.dot((Z-self.H.dot( self.X)).T).T
        self.P = self.P-self.K.dot( self.H ).dot( self.P)


    #our kalman prediction phaze
    def predict(self,Z):
        """
        do the prediction(all first kalman filter)
        input:Z-the resualt of the CCA
        output:none
        """
        self.predictG()
        self.updateG(Z)


    #update stats in kalman faze
    def update(self,Z):
        """
        update the result of prediction after getting result
        input:the data collected
        output:none
        """
        self.updateG(Z)
