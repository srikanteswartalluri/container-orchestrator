
from collections import Counter
from datetime import datetime
from model.infra_config import node_config


def pickNodes(curr_nodes, replicas):
    nodeDetails = getAllHealthyNodes()
    newNodes = []
    ## round robin assignment for now
    n = 0
    tot = len(nodeDetails)
    if tot > 0:
        for i in range(replicas):
            print('Picking node - ',nodeDetails[n])
            curr_nodes.append(nodeDetails[n]['name'])
            newNodes.append(nodeDetails[n]['name'])
            n = (n+1)%tot
    print('Nodes are - ',curr_nodes)
    return newNodes


def getAllHealthyNodes():
    nodes = node_config.objects()
    ## healthy nodes (heart beat update is less than 300 seconds) - change it to 20s
    return [n for n in nodes if ((datetime.utcnow() - n['heart_beat_time']).total_seconds() < 300)]
    ## convert to node map
    ###return {i['name']:i for i in healthyNodes}
