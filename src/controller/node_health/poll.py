from datetime import datetime
from node_health.node_poll import NodeHealth

def pollNodeHealth():
    poll_time = str(datetime.utcnow())
    print(poll_time,'Node Poller: Initiated')
    instance = NodeHealth()
    ## Retrieve failed nodes
    failedNodes = instance.healthCheck()
    print(poll_time,'Node Poller: failed nodes are ', failedNodes)
    container_updates = 0
    if failedNodes:
        ## fetch containers in failed nodes
        container_details = instance.fetchServiceMapCount(failedNodes)
        print(poll_time,'Node Poller: container details are ', str(container_details))
        ## update those containers as well to fail state
        container_updates = instance.updateContainer(failedNodes)
        print(poll_time,'Node Poller: no. of container updates are ', str(container_updates))
        if container_details and container_updates > 0:
            print(poll_time,'Node Poller: Bulk updating service replicas ')
            instance.updateServiceReplicas(container_details)
    print(poll_time,'Node Poller: Finished')

