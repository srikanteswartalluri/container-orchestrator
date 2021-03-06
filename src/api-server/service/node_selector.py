from flask import Response, request, jsonify
from flask_restful import Resource

from util.node_selection import pickNodes

class NodeSelector(Resource):
    def post(self) -> Response:
        """
        POST response method for getting recommended nodes.
        :return: JSON object
        """
        data = request.get_json()
        print('This is deployment service post method!! ', str(data))
        nodes = data['nodes'] if 'nodes' in data else []
        replicas = data['replicas'] if 'replicas' in data else 0
        pickNodes(nodes, replicas)
        return jsonify({'result': nodes})