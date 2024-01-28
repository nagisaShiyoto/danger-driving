import numpy as np
import numpy.linalg


class KalmanFilter:
    def __init__(self, F, Q, H, X, P, R):
        self.F = np.array(F)
        self.Q = np.array(Q)
        self.Ft = np.transpose(F)
        self.H = np.array(H)
        self.Ht = np.transpose(H)
        self.X = np.array(X)
        self.P = np.array(P)
        self.R = np.array(R)
        self.K = []

    def predict(self):
        self.X = self.F @ self.X
        self.P = self.F @ self.P @ self.Ft + self.Q

    def update(self, Z):
        self.K = self.P @ self.Ht @ numpy.linalg.matrix_power((self.H @ self.P @ self.Ht + self.R), -1)
        self.X=self.X- (Z - (self.H @ self.X)@self.K)
        self.P = self.P-self.K @ self.H @ self.P