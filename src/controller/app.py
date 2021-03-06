from node_health.node_poll import NodeHealth
import schedule
import time

from node_health.poll import pollNodeHealth
from state_health.poll import desiredstate

def controller_wrapper():
    ## TODO - figure if previous scheduler still running, if so, do not run again and wait for next timeslot.
    ## TODO - update lock in mongo probably before running pollers
    pollNodeHealth()
    desiredstate()
with open('ca.log', 'w+') as f:
    f.write("\nStarting controller process\n")
    print("\nStarting controller process\n")
schedule.every(120).seconds.do(controller_wrapper)

while True:
    schedule.run_pending()
    time.sleep(1)

#NodeHealth.updateNodes(["node2", "node3", "node0"])