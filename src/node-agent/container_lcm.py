from log_utils import logger
from cli_utils import CLIUtils
from constants import *


class ContainerLcm:
    @staticmethod
    def start_container_on_node(spec):
        (out, err) = CLIUtils.run(START_POD_CONTAINER_SELF_CMD.format(spec["node"], spec["container"]["port"],
                                                                 spec["container"]["image"],
                                                                 spec["container"]["name"]))
        logger.debug('started container id: {}'.format(out))
    @staticmethod
    def list_containers_on_node(node):
        logger.info("Containers on Node co_node_{}: ".format(node))
        (out, err) = CLIUtils.run(LIST_POD_CONTAINERS_CMD.format(node))
        logger.info('list of containers: %s', out)

    @staticmethod
    def list_all_containers():
        port = START_PORT
        for i in range(NUM_WORKER_NODES):
            logger.info("Containers on Node co_node_{}: ".format(port))
            (out, err) = CLIUtils.run(LIST_POD_CONTAINERS_CMD.format(port))
            logger.info('list of containers: %s', out)
            port = port + 1

if __name__ == "__main__":
    clcm = ContainerLcm()
    cont_spec = [{
        "node": "12377",
        "container": {
            "image": "nginx",
            "name": "nginx_12377",
            "port": "12377"
        }
    },
        {
            "node": "12378",
            "container": {
                "image": "nginx",
                "name": "nginx_12378",
                "port": "12378"
            }
        },
    ]
    clcm.start_container_on_node(cont_spec[0])
    clcm.start_container_on_node(cont_spec[1])
    # clcm.list_containers_on_node(cont_spec[0]["node"])
    # clcm.list_containers_on_node(cont_spec[1]["node"])
    clcm.list_all_containers()

