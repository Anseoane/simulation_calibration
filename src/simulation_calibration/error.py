import numpy as np

class ErrorMetrics:

    def __init__(self, ground_truth, simulation):
        self.ground_truth = ground_truth
        self.simulation = simulation

    def rmse_segment_error(self):
        
        pass

    def segment_weights(self):
        pass

    def global_error(self, segment_errors, segment_weights):
        return np.sum(segment_errors * segment_weights)