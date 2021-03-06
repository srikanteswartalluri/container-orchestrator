import sys
import os

node = sys.argv[1]
wn_node_map = {"co_node_12375": "worker_node_1",
               "co_node_12376": "worker_node_2",
               "co_node_12377": "worker_node_3",
               "co_node_12378": "worker_node_4",
               "co_node_12379": "worker_node_5"}
os.system("docker-compose up -d {}".format(wn_node_map[node]))
os.system("docker exec {0} python3 /NodeAgent.py -n {0} -p &".format(node))
os.system("docker exec {0} python3 /NodeAgent.py -n {0} -c &".format(node))
