# container-orcherstrator
#### video demo: https://www.youtube.com/watch?v=F04XxY2kVEE
#### To bring up a cluster 
<code>
./src/node-agent/utils/start_cluster.sh
</code>

This brings up a master node and 5 worker nodes. 
Nodes here refer to the containers running service. This solution relies on docker-compose
and the specification of each node is maintained under ./docker-compose.yml

  * #### API Server: 
    This is responsible to expose the following APIs:
      * service
      * state
      * node_state
      * container_state
      * service_state
      #### Functionality of API Server  
      * Once the API is recived: 
        * calls lib to get healthy nodes (no. of replicas)
        * DB entry -> service_config
        * DB entry -> container_config with state ‘in queue’
        * Send messages to exchange with routing key(node Id)
  * #### Mongo DB
    This is the backbone Database for the orchestrator to store the states of 
    worker nodes, containers and services
    Collections:
    * node_config
    * container_config
    * service_config
  DB is backed by a persistent volume which gives immunity from container failures to retain config.
      
    
  * #### Rabbit MQ server
    This is the mechanism to pass the messages from the API server(producer) to
    the designated worker nodes(consumers) to bring up containers
    
  * #### Worker Nodes
    These worker nodes are containers by themselves running docker:dind image.
    There is a node agent process running the following
    * Rabbit MQ consumer
      checks container_details in this node 
        * if (state is ‘in queue’)
          * it will process the configuration -> bring up container replica
          * update DB entry, container_config - state to completed or failed depending on exception
          * update DB entry, service_config - increment current_state
        * elif (stat is 'fail')
          * stop the container replica
      
    * Poller to update the node heartbeat time every 5s in the DB(node_config collection).
  
  * #### Controller
    This components runs two pollers
    * Poller1: Checks for any node failures(hearbeat time update > 5 sec) and 
      mark the containers on that node as 'fail' in the DB(container_config collection)
      and reduce the current_state in the DB(service_config collection).
    * Poller 2: checks service_config collection (current state == replicas), if not, 
      Query that container detail from all nodes and check its status
      If status is in-queue, check last state updated time -> if delta is beyond threshold (1 min), change state to ‘failed’
      Capture the count of failed states, update service_config current_state to replicas- failed_state.
      send request to api server with failed_state_count to achieve desired state by deciding healthy nodes  
  * #### Infra container
    This is a temporary container that comes up during the start to 
    run the automation required to perform the following:
    * Create Rabbit MQ exchange(co_topic)
    * Create Rabbit MQ queues for each worker node(co_node_*) and bind them to exchange(co_topic)
    * Start node agent on the worker nodes
  




#### Bring up a service

Invoke the post API as shown in the following example:
##### POST URL: 
http://127.0.0.1:5000/service

##### body:
<code>
{
"services": [{
"serviceName": "alpine-new-name27",
"replicas" : 3,
 "container": 
     {
    "name": "alpine-int27",
    "image": "nginx"
    }
 }]
}
</code>

We can check DB and Rabbit MQ queues that API server allocates worker nodes on which 
container has to be brought up and messages are dispatched with appropriate keys.

Each node agent consumes the messages from the respective queues to bring up the containers 
and updates DB with container state as 'running'.


#### Bring down a node and containers rebalance for a service

While the service is running and desired state is achieved, let's bring down a worker node
where a container is running. Controller tries to bring the service to desired state by 
bringing up the containers on other healthy worker nodes.

#### Edit a service (scale up /down)

While the service is running, If an API is received to increase or decrease the no. of
replicas, contoller tries to achieve desired state by spinning up new containers or 
remove the existing containers


#### Bringing the failed worker node up and invoke a new service bring up API
Node that came up should be available for new containers spin up.


  






