import numpy as np


class KalmanFilter:

    def __init__(self, F, B, Q):
        self.F = F
        self.B = B
        self.Q = Q
        self.Ft = np.transpose(F)
        #sel

    def prediction_kalman(self):
        return 0
