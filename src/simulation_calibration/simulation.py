import traci as libsumo

class Simulation:
    def __init__(self, sumo_network, demand_definition):
        self.sumo_network = sumo_network
        self.demand_definition = demand_definition

    def run(self):
        """
        Executes the simulation. 
        Returns SimulationResults
        """ 



class SimulationResults:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def get_by_arbitrary_interval(interval, magnitude):
        results_dict = {}
        return results_dict

