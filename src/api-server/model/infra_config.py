# mongo-engine packages
from mongoengine import Document, StringField, ListField, IntField
from mongoengine.fields import DateTimeField, FloatField

class service_config(Document):
    '''
        serviceName
        current_state
        Replicas
        node_list -> which all nodes were picked to deploy
    '''
    name = StringField()
    description = StringField(max_length=240)
    cimage = StringField()
    cname = StringField()
    current_state = IntField()
    replicas = IntField()
    nodes = ListField(StringField())

class container_config(Document):
    '''
        Name
        State
        node_mapping
        Image
        Last State updated time
    '''
    name = StringField()
    state = StringField()
    node_mapping = StringField()
    image = StringField()
    last_state_update_time = DateTimeField()
    service_map = StringField()

    def __repr__(self):
        return repr('Hello ' + self.name )

class node_config(Document):
    '''
        Node id
        Description
        Last state updated (heart beat)
    '''
    name = StringField()
    description = StringField()
    heart_beat_time = DateTimeField()
    free_mem = FloatField()
    free_cpu = FloatField()
    free_disk = FloatField()
