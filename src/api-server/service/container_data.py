# flask packages
from util.producer import ExternalQueue
from flask import Response, request, jsonify
from flask_restful import Resource
from model.infra_config import container_config

class containerConfig(Resource):
    @staticmethod
    def get() -> Response:
        output = container_config.objects()
        return jsonify({'result': output})

    def post(self) -> Response:
        """
        POST response method for creating container configuration objects.
        :return: JSON object
        """
        print('This is container config post method!! ', request.get_json)
        data = request.get_json()
        post_user = container_config(**data).save()
        output = {'id': str(post_user.id)}
        # Send configuration to queue
        print(str(data))
        return jsonify({'result': output})
        