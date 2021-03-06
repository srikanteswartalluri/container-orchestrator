#!/usr/bin/python
from log_utils import logger
from cli_utils import CLIUtils
from constants import *


cont_spec = {
    "node": "12375",
    "container": {
        "image": "nginx",
        "name": "nginx_12375",
        "port": "12374"
    }
}
num_nodes = 5
num_replicas = 3
port = START_PORT
# for i in range(int(num_replicas)):
#     cont_port = START_PORT
#     image_name = "nginx"
#     # for i in range(int(num_replicas)):
#     #     cont_name = "{}_{}".format(image_name, cont_port)
#     #     (out, err) = CLIUtils.run(START_POD_CONTAINER_CMD.format(port, cont_port, image_name, cont_name))
#     #     logger.debug('started container id: {}'.format(out))
#         # cont_port = cont_port + 1
#     cont_name = "{}_{}".format(image_name, cont_port)
#     (out, err) = CLIUtils.run(START_POD_CONTAINER_CMD.format(port, cont_port, image_name, cont_name))
#     logger.debug('started container id: {}'.format(out))
#     port = port + 1
(out, err) = CLIUtils.run(START_POD_CONTAINER_CMD.format(cont_spec["node"], cont_spec["container"]["port"], cont_spec["container"]["image"], cont_spec["container"]["name"]))
logger.debug('started container id: {}'.format(out))

port = START_PORT
for i in range(int(num_nodes)):
    logger.info("Containers on Node co_node_{}: ".format(port))
    (out, err) = CLIUtils.run(LIST_POD_CONTAINERS_CMD.format(port))
    logger.info('list of containers: %s', out)
    port = port + 1



