from .strategy import Strategy

class Port_Num_Strategy(Strategy):
    """ Evaluates the list of open ports and recommends exploits based on prior success. """

    def __init__(self, exploits:list):
        self.weights = {}
        for exploit_name in exploits:
            self.weights[exploit_name] = {}

    # ranks exploits by past success given list of open ports
    def search(self, target_data:dict):
        weight_sums = {}

        for exploit in self.weights:
            weight_sums[exploit] = 0
            for port in target_data["ports"]:
                port_num = int(port["portNum"])
                weight_sums[exploit] += self.weights[exploit].get(port_num, 0) # 0 if not present

        exploits = sorted(weight_sums, key=(lambda key: weight_sums[key]), reverse=True)
        print("port_nums search: weight_sums = {}".format(weight_sums))
        return exploits

    # increases weights for each port on exploit success, decreases on failure
    def update(self, target_data:dict, exploit_name:str, result:bool):
        for port in target_data["ports"]:
            port_num = int(port["portNum"])

            if result:
                updated = self.weights[exploit_name].get(port_num, 4)
                updated = min(updated + 1, 10)
                self.weights[exploit_name][port_num] = updated
            else:
                updated = self.weights[exploit_name].get(port_num, 0)
                updated = max(updated - 1, 0)
                self.weights[exploit_name][port_num] = updated

        print("port_nums update: weights = {}".format(self.weights))