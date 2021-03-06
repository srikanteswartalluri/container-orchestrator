
from collections import Counter
from util.common import insert_containers, insert_service_config, update_service_config, pickNodes
from mongoengine.queryset.visitor import Q
from util.producer import ExternalQueue
from flask import Response, request, jsonify
from flask_restful import Resource
from model.infra_config import container_config, service_config

class deployment(Resource):

    def post(self) -> Response:
        """
        POST response method for intiating deployments.
        :return: JSON object
        """
        data = request.get_json()
        print('This is deployment service post method!! ', str(data))
        
        ### Check if its an array or single object
        '''
            Deployments can be requested by user/client or controller (- to achieve desired state)
        '''
        if 'services' in data:
            print('Multiple services detected! Processing every record....')
            for service in data['services']:
                c_list = []
                existing = service_config.objects(name=service['serviceName'])
                if not existing:
                    '''
                        New service requested
                        -> Get the nodes based on replicas
                        -> Insert record in service_config collection
                        -> Insert records in container_config collection
                        -> Send the container record to rabbit exchange with appropriate node as routing key
                    '''
                    s_nodes = []
                    deploy_nodes = pickNodes(s_nodes, service['replicas'])
                    print('Nodes inserted into service config -- ', s_nodes)
                    print('Nodes where containers will be deployed -- ', deploy_nodes)
                    insert_service_config(service, s_nodes)
                    if deploy_nodes:
                        c_list = insert_containers(service, deploy_nodes)
                        for c in c_list:
                            print('Sending data to queue ', )
                            ## Send data to rabbit exchange
                            ExternalQueue.sendMessage(c.to_json(), c['node_mapping'])

                else:
                    '''
                        Request for changing existing service configuration. There are 3 scenarios -
                        1) no. of replicas = number of running/in-queue containers - Nothing to process since desired state is achieved
                        2) no. of replicas > number of running/in-queue containers - Process to bring up delta containers to achieve desired state
                        3) no. of replicas < number of running/in-queue containers - Process to destroy extra containers to achieve desired state
                    '''
                    ## Check if image name and container are same, ideally existing service metadata shouldn't change except change in replicas
                    if existing[0]['cimage'] != service['container']['image'] or existing[0]['cname'] != service['container']['name']:
                        return jsonify({'result': 'Request failed for the service '+service['serviceName']+'... Since image/container name does not match with existing one, hence further service requests are dropped'})
                    
                    valid_container_list = container_config.objects(Q(service_map=service['serviceName']) & Q(state__ne='fail'))
                    len_containers = len(valid_container_list)
                    print('Existing valid containers size is -- ', len_containers)

                    if len_containers == service['replicas']:
                        print('Scenario 1: replicas = no. of running/in-queue containers... Just update config to ensure accurate data and do nothing!')
                        update_service_config(service, existing[0]['nodes'], len_containers)

                    elif len_containers < service['replicas']:
                        '''
                            -> Pick additional nodes to achieve desired state
                            -> Track current state with running containers
                            -> update service config with latest information
                            -> Insert missing container records
                            -> track additional containers and push it to exchange with node as routing key 
                        '''
                        print('Scenario 2: replicas > no. of running/in-queue containers...!')
                        s_nodes = []
                        latest_curr_state = 0
                        for c in valid_container_list:
                            s_nodes.append(c['node_mapping'])
                            if c['state'] != 'queue':
                                latest_curr_state += 1
                        
                        ## TODO: Track current state here
                        deploy_nodes = pickNodes(s_nodes, service['replicas']-len_containers)
                        print('Nodes inserted into service config -- ', s_nodes)
                        print('Nodes where containers will be deployed -- ', deploy_nodes)
                        update_service_config(service, s_nodes, latest_curr_state)
                        if deploy_nodes:
                            c_list = insert_containers(service, deploy_nodes)
                            for c in c_list:
                                print('Sending data to queue ', c)
                                ## Send data to rabbit exchange
                                ExternalQueue.sendMessage(c.to_json(), c['node_mapping'])

                    else:
                        '''
                            -> Fail extra containers, change state to 'fail'
                            -> eliminate appropriate nodes from list for failed containers
                            -> figure out current state according to what kind of containers failed
                            -> update service config with latest information
                            -> push the failed one's to exchange with node as routing key 
                        '''
                        print('Scenario 3: replicas < no. of running/in-queue containers...!')
                        extra_c = len_containers - service['replicas']
                        print('explicit failing container count - ', str(extra_c))
                        latest_curr_state = 0
                        
                        s_nodes = []
                        for v_c in valid_container_list:
                            if extra_c > 0:
                                data = v_c.update(state='fail')
                                extra_c -= 1
                                v_c['state'] = 'fail'
                                print('Sending data to queue ', v_c)
                                ## Send data to rabbit exchange
                                ExternalQueue.sendMessage(v_c.to_json(), v_c['node_mapping'])
                                
                            else:
                                s_nodes.append(v_c['node_mapping'])
                                if v_c['state'] != 'queue':
                                    latest_curr_state += 1
                        
                        update_service_config(service, s_nodes, latest_curr_state)
                        
        return jsonify({'result': 'Your request will be processed!'})
        