from settings import params
import torch
import argparse
from env.environment import Environment
from agent.algorithm import make
import train
from Q_Optimizing_Network import MixingQ
# from Mixing_net import mixing_net
# import sys
# sys.path.append(r'./Informer-MVP')
from settings import args as parses
import os
import csv


# def parse_args():
#     parser = argparse.ArgumentParser("Experiments for pursuit SUMO environments")
#     parser.add_argument("--exp_name", type=str, default="test", help="addition name of the experiment")  # 实验名
#     parser.add_argument("--port", type=int, default=8813, help="The port of sumo environment")
#     parser.add_argument("--batch_size", type=int, default=32, help="The train batch size")
#     parser.add_argument("--domain_name", type=str, default="3x3Traffic", help="The domain of training")
#     parser.add_argument("--alg_name", type=str, default="PPO", help="The algorithm name of training")
#     parser.add_argument("--reload_exp", type=str, default=None, help="The reload exp name")
#     parser.add_argument("--test", action="store_true", default=False, help="Test")
#     parser.add_argument("--gui", action="store_true", default=False, help="Use gui")
#
#     return parser.parse_args()

# parses = parse_args()

# if parses.domain_name == "3x3":
#     params["rou_path"] = "./env/3x3/3x3Grid.rou.xml"
#     params["cfg_path"] = "./env/3x3/3x3Grid.sumocfg"
#     params["net_path"] = "./env/3x3/3x3Grid.net.xml"
# elif parses.domain_name == "3x3Qco":
#     params["rou_path"] = "./env/3x3Qco/3x3Grid.rou.xml"
#     params["cfg_path"] = "./env/3x3Qco/3x3Grid.sumocfg"
#     params["net_path"] = "./env/3×3Qco/3x3Grid.net.xml"
#     params["num_pursuit"] = 4
#     params["pursuit_ids"] = ["p0", "p1", "p2", "p3"]
#     params["num_evader"] = 2
#     params["evader_ids"] = ["e0", "e1"]
#     params["code_length"] = 6
#     params["num_action"] = 3
#     params["local_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
#     params["global_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
# elif parses.domain_name == "3x3Traffic":
#     params["rou_path"] = "./env/3x3Traffic/3x3Grid.rou.xml"
#     params["cfg_path"] = "./env/3x3Traffic/3x3Grid.sumocfg"
#     params["net_path"] = "./env/3x3Traffic/3x3Grid.net.xml"
#     params["num_pursuit"] = 4
#     params["pursuit_ids"] = ["p0", "p1", "p2", "p3"]
#     params["num_evader"] = 2
#     params["evader_ids"] = ["e0", "e1"]
#     params["code_length"] = 6
#     params["num_action"] = 3
#     params["local_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
#     params["global_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
# elif parses.domain_name == "4x4Traffic":
#     params["rou_path"] = "./env/4x4Traffic/4x4Grid.rou.xml"
#     params["cfg_path"] = "./env/4x4Traffic/4x4Grid.sumocfg"
#     params["net_path"] = "./env/4x4Traffic/4x4Grid.net.xml"
#     params["num_pursuit"] = 4
#     params["pursuit_ids"] = ["p0", "p1", "p2", "p3"]
#     params["num_evader"] = 2
#     params["evader_ids"] = ["e0", "e1"]
#     params["code_length"] = 7
#     params["num_action"] = 3
#     params["local_observation_shape"] = (params["num_pursuit"] + params["num_evader"], 4*params["code_length"] + 1 + 80)
#     params["global_observation_shape"] = (params["num_pursuit"] + params["num_evader"], 4*params["code_length"] + 1 + 80)


params["rou_path"] = "./env/3x3Traffic/3x3Grid.rou.xml"
params["cfg_path"] = "./env/3x3Traffic/3x3Grid.sumocfg"
params["net_path"] = "./env/3x3Traffic/3x3Grid.net.xml"
params["num_pursuit"] = 4
params["pursuit_ids"] = ["p0", "p1", "p2", "p3"]
params["num_evader"] = 2
params["evader_ids"] = ["e0", "e1"]
params["code_length"] = 6
params["num_action"] = 3
params["local_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
params["global_observation_shape"] = (params["num_pursuit"]+params["num_evader"], 25+48)
params["port"] = parses.port
params["gui"] = parses.gui
params["domain_name"] = parses.domain_name
params["algorithm_name"] = parses.alg_name
params["exp_name"] = parses.exp_name
params["batch_size"] = parses.batch_size
params["use_pre"] = parses.use_predict
params["pre_format"] = parses.pre_format
params["assign_method"] = parses.assign_method
params["no_task"] = parses.no_task
params["pre_method"] = parses.pre_method
params["directory"] = "output/{}-domain-{}-{}".format(params["domain_name"], params["algorithm_name"], params["exp_name"])

params["env"] = Environment(params)
controller = make(params["algorithm_name"], params)

QON=MixingQ(params)


if parses.test:
    reload_model_path = os.path.join("output", "3x3Traffic-domain-DQN_all", "best.pth")
    if os.path.exists(reload_model_path):
        params["test_output_csv"] = os.path.join("output", "3x3Traffic-domain-DQN_all", "best_res.csv")
        with open(params["test_output_csv"], "a+", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["steps", "reward"])
            csvfile.close()
        controller.load_weights_from_history(reload_model_path)
        print("Load model success form", reload_model_path)
        result = train.test(controller, params, 100)
else:
    result = train.run(controller, params, QO_net=QON)









