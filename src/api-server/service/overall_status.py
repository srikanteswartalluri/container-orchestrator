# flask packages
from util.producer import ExternalQueue
from flask import Response, request, jsonify
from flask_restful import Resource
from model.infra_config import service_config
from model.infra_config import node_config
from model.infra_config import container_config


class overallState(Resource):
    @staticmethod
    def get() -> Response:
        service_objects = service_config.objects()
        node_objects = node_config.objects()
        container_objects = container_config.objects()
        containers = [{c['name']: c['state']} for c in container_objects]
        nodes = [{n['name']: n['heart_beat_time']} for n in node_objects]
        services = [{s['name']: "{}/{}".format(s["current_state"], s["replicas"])} for s in service_objects]
        output = {"containers" : containers,
                  "services": services,
                  "nodes": nodes}
        return jsonify({'result': output})
