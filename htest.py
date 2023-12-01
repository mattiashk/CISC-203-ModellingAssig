import json
import sat_solver
import utils
from bauhaus.utils import count_solutions, likelihood

with open('tests.config.json', 'r') as config_file:
        config = json.load(config_file)
        #for testcase in config:
        for i in range(1, len(config)):
            testcase = config[i]
            O = utils.create_data_layer("data/testing/test-small-general")
            #O = utils.create_data_layer(testcase["location"])
            result = sat_solver.execute(O)
            print(count_solutions(result["Theory"]))