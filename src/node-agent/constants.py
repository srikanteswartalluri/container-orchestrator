START_PORT=12375
START_WORKER_NODE_CMD="docker run --rm --name=co_node_{0} --network=container-orch_co --privileged -p {0}:2375 -d -e DOCKER_TLS_CERTDIR=\"\" dindpy3"
LIST_NODES_CMD="docker ps -f \"name=co_node*\""
KILL_NODE_CMD="docker kill {}"
START_POD_CONTAINER_CMD="DOCKER_HOST=tcp://localhost:{0} docker run --rm --name {3} -v /Users/srikanteswararaotalluri/html:/usr/share/nginx/html:ro -p {1}:80 -d {2}"
LIST_POD_CONTAINERS_CMD="DOCKER_HOST=tcp://localhost:{} docker ps"
NUM_WORKER_NODES=5
START_POD_CONTAINER_SELF_CMD="docker run --rm --name {3}  -p {1}:80 -d {2}"