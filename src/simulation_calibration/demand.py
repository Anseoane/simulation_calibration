from dataclasses import dataclass

import numpy as np


class Demand:
    total_veh_num: int



class DemandGenerator:
    """
    Creates a Demand definition
    """
    def __init__(self, idm_params, route_weights, t_start, t_end):
        self.idm_params = idm_params
        self.route_weights = route_weights
        self.t_start = t_start
        self.t_end = t_end

    def _calculate_od_probs(self):
        pass

    def apply_vtype_params(self, params, ):
        pass

    

        
