#!/usr/bin/python
from log_utils import logger
from cli_utils import CLIUtils
from constants import *


(out, err) = CLIUtils.run(LIST_NODES_CMD)
logger.debug('list of containers: {}'.format(out))
lines = out.strip().split("\n")
for i in range(1, len(lines)):
    container_id = lines[i].split()[0]
    (out, err) = CLIUtils.run(KILL_NODE_CMD.format(container_id))
    logger.info("{} killed".format(container_id))



