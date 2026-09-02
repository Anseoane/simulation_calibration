class DemandGenerator:
    """Takes the information regarding the network and the """
    def __init__(self, idm_params, route_weights, t_start, t_end):
        self.idm_params = idm_params
        self.route_weights = route_weights
        self.t_start = t_start
        self.t_end = t_end
        self.delta_t = t_end - t_start

    def _calculate_od_probs(self):
        pass

    

        
