from collections import Counter
import datetime
import requests

from util.db import db
from node_health.node_poll import NodeHealth

class StateHealth:
    def desiredStateCheck(self):
        ## filter services if current_state not same as replicas
        inconsistent_services = db.service_config.find({
                        "$expr" : {
                            "$ne": ["$current_state", "$replicas"]
                        }
                    })
        details = []
        names = []
        for item in inconsistent_services:
            details.append(item)
            names.append(item['name'])
        return names, details

    def analyzeContainerInQueueState(self, services):
        containerList = db.container_config.find(
            {
                "$and": [
                    {
                        "service_map" : {
                            "$in": services
                        }
                    },
                    {
                        "state" : {
                            "$eq": "queue"
                        }
                    }
                ]
            }
        )

        ## consider container as failed state if it was not created in 5 mins by node agent
        failedContainers = [container['_id'] for container in containerList 
                        if ((datetime.datetime.utcnow() - container['last_state_update_time']).total_seconds() > 300)]
        print(failedContainers)

        records = db.container_config.update_many(
            {
                "_id" : {
                    "$in": failedContainers
                }
            },
            {
                "$set": {
                    "state": "fail"
                }
            }
        )
        if records:
            print('Total container records modified for long duration in-queue state are - ',str(records.modified_count))
        else:
            print('No container records modified to failed state for long duration in-queue state')

    def constructDesiredState(self, service_names, service_details):
        ## Query for running containers + containers in queue for short time (valid scenario)
        r_c = db.container_config.find({
            "$and": [
                    {
                        "service_map" : {
                            "$in": service_names
                        }
                    },
                    {
                        "state" : {
                            "$ne": "fail"
                        }
                    }
                ]
        })
        running_containers = list(r_c)
        serviceCountMap = Counter([item['service_map'] for item in running_containers])
        print('Service count map of running containers - ', dict(serviceCountMap))
        
        '''
            Compare inconsistent_services (current_state != replicas) with serviceCountMap (no of containers in running and queue state)
            if serviceCountMap value is same as replicas, then ignore those services are they are not inconsistent at the moment; since
            some containers are in queue state and they have more time to process them until they reach the thresold (5 min) mark. 
        '''
        unhealthy_service_details = [s for s in service_details if s['replicas'] != (0 if not serviceCountMap[s['name']] else serviceCountMap[s['name']])]
        unhealthy_service_names = set([s['name'] for s in unhealthy_service_details])
        print('Actual unhealthy services are - ', unhealthy_service_names)

        ''' 
            Build data structure - service as the key and the nodes where containers are already running 
            so that it can be used later for building request to API server
        '''
        # serviceContainerMap = {}
        # for ct in running_containers:
        #     if ct['service_map'] in unhealthy_service_names:
        #         if ct['service_map'] not in serviceContainerMap:
        #             serviceContainerMap[ct['service_map']] = {}
        #             serviceContainerMap[ct['service_map']]['nodes'] = []

        #         ## append success nodes to service map
        #         serviceContainerMap[ct['service_map']]['nodes'].append(ct['node_mapping'])

        # print('Service Container-Node mapping for valid ones - ', serviceContainerMap)
        ## Build request for API server
        if unhealthy_service_names:
            api_server_request = []
            for item in unhealthy_service_details:
                request = {}
                request['serviceName'] = item['name']
                request['replicas'] = item['replicas']
                request['container'] = {}
                request['container']['name'] = '' if 'cname' not in item else item['cname']
                request['container']['image'] = '' if 'cimage' not in item else item['cimage']
                api_server_request.append(request)

            ## Call API server
            service_request = {}
            service_request['services'] = api_server_request
            print('API server request will be processed with the following details ----- ')
            print(service_request)
            url = 'http://co_api:5000/service'
            resp = requests.post(url, json=service_request)
            print('Response status code ', resp.status_code)
            





