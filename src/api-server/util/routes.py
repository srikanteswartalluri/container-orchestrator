# flask packages
from service.deployments import deployment
from flask_restful import Api

# project resources
from service.node_selector import NodeSelector
from service.services_config import serviceConfig
from service.node_config import nodeConfig
from service.container_data import containerConfig
from service.overall_status import overallState

def create_routes(api: Api):
    """Adds resources to the api.
    :param api: Flask-RESTful Api Object
    :Example:
        api.add_resource(HelloWorld, '/', '/hello')
        api.add_resource(Foo, '/foo', endpoint="foo")
        api.add_resource(FooSpecial, '/special/foo', endpoint="foo")
    """
    api.add_resource(NodeSelector, '/recommendNodes')
    api.add_resource(deployment, '/service')
    api.add_resource(serviceConfig, '/service_state')
    api.add_resource(nodeConfig, '/node_state')
    api.add_resource(containerConfig, "/container_state")
    api.add_resource(overallState, "/state")