import numpy as np

class KalmanFilter:

    def __init__(self, F, B, Q, K):
        self.F = F
        self.B = B
        self.Q = Q
        self.K = K

        self.Ft = np.linalg.inv(F)


    def prediction_kalman():
