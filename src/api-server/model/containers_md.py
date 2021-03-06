# mongo-engine packages
from mongoengine import Document, StringField, FloatField, DateTimeField, IntField, ListField


class Nodes(Document):
    """
    Template for a mongoengine document.
    :param name: required string value
    :param description: optional string value, fewer than 120 characters
    :param ram: optional float value
    :param processor: optional string
    """
    _id = IntField(required=True)
    name = StringField(required=True)
    status = StringField(max_length=240)
    last_status_update = DateTimeField(required=True)


class Containers(Document):
    """
    Template for a mongoengine document.
    :param name: required string value
    :param description: optional string value, fewer than 120 characters
    :param ram: optional float value
    :param processor: optional string
    """
    _id = IntField(required=True)
    name = StringField(required=True)
    status = StringField(max_length=240)
    last_status_update = DateTimeField(required=True)


class ConfigDetails(Document):
    """
    Template for a mongoengine document.
    :param name: required string value
    :param description: optional string value, fewer than 120 characters
    :param ram: optional float value
    :param processor: optional string
    """
    _id = IntField(required=True)
    service = StringField(required=True)
    current_state = IntField()
    desired_state = IntField()
    node_list = ListField()