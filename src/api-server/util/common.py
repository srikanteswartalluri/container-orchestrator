
from collections import Counter
from datetime import datetime
from model.infra_config import container_config, node_config, service_config
import uuid


'''
    Node recommendation in round robin with no of replicas
    curr_nodes are existing nodes and new picked ones are appended to it
    it will also return list of picked ones so that this list can be used for queues
'''
def pickNodes(curr_nodes, replicas):
    nodeDetails = getAllHealthyNodes()
    newNodes = []
    ## round robin assignment for now
    n = 0
    tot = len(nodeDetails)
    if tot > 0:
        for i in range(replicas):
            nodeName = nodeDetails[n]['name']
            print('Picking node hello - ',nodeDetails[n].to_json())
            curr_nodes.append(nodeName)
            newNodes.append(nodeName)
            n = (n+1)%tot
    print('Nodes are - ',curr_nodes)
    return newNodes


def getAllHealthyNodes():
    nodes = node_config.objects()
    ## healthy nodes (heart beat update is less than 300 seconds) - change it to 20s
    return [n for n in nodes if ((datetime.utcnow() - n['heart_beat_time']).total_seconds() < 60)]


def update_service_config(service_info, s_nodes, c_state):
    output = service_config.objects(name=service_info['serviceName']).update(
                    nodes=s_nodes,
                    current_state=c_state,
                    replicas=service_info['replicas'])
    print('Updated service configuration ',output)

def insert_service_config(service_info, s_nodes):
    instance = service_config()
    instance.name = service_info['serviceName']
    instance.replicas = service_info['replicas']
    instance.current_state = 0
    instance.cimage = service_info['container']['image']
    instance.cname = service_info['container']['name']
    instance.nodes = s_nodes
    output = instance.save()
    print('Inserted services data ', output.to_json())

def insert_containers(service_info, s_nodes):
    containers = []
    for n in s_nodes:
        new_ctr = container_config()
        new_ctr.name = service_info['container']['name'] + str(uuid.uuid4())
        new_ctr.image = service_info['container']['image']
        new_ctr.node_mapping = n
        new_ctr.service_map = service_info['serviceName']
        new_ctr.state = 'queue'
        new_ctr.last_state_update_time = datetime.utcnow()
        containers.append(new_ctr)
    output = container_config.objects.insert(containers)
    print('Inserted all the containers ', output)
    return output

def update_state_to_fail_containers(c_names):
    output = container_config.objects(name__in=c_names).update(state='fail')
    print('Updated containers to failed state ', output)
    return output

