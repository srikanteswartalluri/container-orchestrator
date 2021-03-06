import argparse
from NodeAgent import NodeAgent
na = NodeAgent("test")
parser = argparse.ArgumentParser(description="Node agent's arguments")
parser.add_argument("-n", help="name of the node")
parser.add_argument("-p", action="store_true", help="start node agent poller")
parser.add_argument("-c", action="store_true", help="start queue consumer")
args = parser.parse_args()
print(args)
if args.p:
    na.start_poller()
if args.c:
    na.start_consumer()