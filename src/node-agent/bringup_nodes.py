#!/usr/bin/python3
import sys
from log_utils import logger
from cli_utils import CLIUtils
from constants import *
from NodeAgent import NodeAgent
import pika
import datetime


if len(sys.argv) < 2:
   logger.info("Enter the number of nodes to bring up")
   logger.info("./bringup_nodes.py <num_nodes>")
   sys.exit(1)
num_nodes = sys.argv[1]

# create exchange
connection = pika.BlockingConnection(
    pika.ConnectionParameters('coqueue', 5672, '/', pika.PlainCredentials("root", "root123")))
channel = connection.channel()
channel.exchange_declare('co_topic')

port = START_PORT
for i in range(int(num_nodes)):
    node_name = "co_node_{}".format(port)
    na = NodeAgent(node_name)
    na.nodes.insert_one({"name": node_name,
    "description" : "worker node",
    "heart_beat_time" : datetime.datetime.utcnow(),
    "free_mem" : 10,
    "free_cpu" : 4,
    "free_disk" : 128})
    logger.debug('added worker node container')
    # create queues
    channel.queue_declare(node_name)
    # bind the queue to exchange
    channel.queue_bind(node_name,'co_topic',routing_key=node_name)
    # start node agent
    cmd= "python3 /NodeAgent.py -n {} -c &".format(node_name)
    d_cmd = "docker exec {} {}".format(node_name, cmd)
    print(d_cmd)
    CLIUtils.run_nb(d_cmd)
    # start node agent poller
    cmd = "python3 /NodeAgent.py -n {} -p &".format(node_name)
    d_cmd = "docker exec {} {}".format(node_name, cmd)
    print(d_cmd)
    CLIUtils.run_nb(d_cmd)

    port = port + 1

