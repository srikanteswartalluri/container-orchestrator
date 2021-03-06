from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
import json
import pika
from cli_utils import CLIUtils
import schedule
import time
import datetime
import argparse
import re


class NodeAgent:
    def __init__(self, node):
        c = MongoClient(host=['co_repo:27017'], username="root", password="root123")
        self.mydb = c["co_db"]
        self.nodes = self.mydb["node_config"]
        self.containers = self.mydb["container_config"]
        self.config_details = self.mydb["service_config"]
        self.node = node

    def update_container(self, id, state, last_state_update_time):
        filt = {"_id": ObjectId(id["$oid"])}
        update = {"$set":{"state": state, "last_state_update_time": last_state_update_time}}
        return self.containers.update_one(filt, update)

    def update_node(self):
        filt = {"name": self.node}
        update = {"$set": {"heart_beat_time": datetime.datetime.utcnow()}}
        return self.nodes.update_one(filt, update)

    def update_config_details(self, service):
        filt = {"name": service}
        # svc = self.config_details.find(filt)
        # cs = svc[0]["current_state"]
        # # nl = svc[0]["nodes"]
        # new_state = int(cs) + 1
        # # nl.append(self.node)
        # filt = {"name": service}
        # update = {"$set": {"current_state": new_state}}#, "node_list": nl}}
        update = {"$inc": {"current_state": 1}}
        # self.config_details.update_one(filt, update)
        return self.config_details.update_one(filt, update)


    def list_nodes(self):
        for i in self.nodes.find():
            print(i)
    def list_containers(self):
        for i in self.containers.find():
            print(i)
    def list_config_details(self):
        for i in self.config_details.find():
            print(i)
    def _stop_container(self, name):
        cmd = "docker stop {}".format(name)
        CLIUtils.run_nb(cmd)

    def _check_container_state_in_db(self, id):
        filt = {"_id": ObjectId(id["$oid"])}
        print(filt)
        svc = self.containers.find(filt)
        print(svc)
        return str(svc[0]["state"])

    def start_consumer(self):
        print("start consumer")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('coqueue', 5672, '/', pika.PlainCredentials("root", "root123")))
        channel = connection.channel()

        def callback(ch, method, properties, body):
            with open('na.log', 'a+') as f:
                print(dir(body))
                print(f'{body}  are received')

                f.write(f'{body}  are received\n')
                payload = json.loads(body.decode('utf-8'))
                f.write("state in payload: {}\n".format(payload["state"]))
                f.write("_id in payload: {}\n".format(payload["_id"]))
                if payload['state'] == "fail":
                    #delete the container if running
                    f.write("Received failed state. Stopping container\n")
                    self._stop_container(payload['name'])
                else:
                    # check the db for the state of the container
                    f.write("checking the state in db: {} \n".format(self._check_container_state_in_db(payload["_id"])))
                    if self._check_container_state_in_db(payload["_id"]) == 'queue':
                        print("Bringing up the container {}".format(payload['image']))
                        f.write("Bringing up the container {}\n".format(payload['image']))
                        cmd = "docker run --rm --name={} -d {}".format(payload["name"], payload['image'])
                        out, err = CLIUtils.run(cmd)
                        f.write("Executed cmd: {}".format(cmd))
                        f.write("Out put : {}\n".format(out))
                        f.write("Err: {}\n".format(err))
                        if self._check_container_state_in_db(payload["_id"]) == 'queue':
                            f.write("Updating container state in db: {}\n".format(payload['name']))
                            out = self.update_container(payload["_id"], "running", datetime.datetime.utcnow())
                            f.write("update container out put : {}\n".format(out))
                            f.write("Updating service current_state in db: {}\n".format(payload['name']))
                            out = self.update_config_details(payload["service_map"])
                            f.write("update config details out put: {}\n".format(out.raw_result))
                        else:
                            # clean the stale container
                            f.write("stopping container on node as the scheduler has marked it stale in db: {}\n".format(payload['name']))
                            self._stop_container(payload["name"])

        channel.basic_consume(queue=self.node, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        # channel.

    def start_poller(self):
        print("start poller")
        schedule.every(5).seconds.do(na.update_node)
        while True:
            schedule.run_pending()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Node agent's arguments")
    parser.add_argument("-n", help="name of the node")
    parser.add_argument("-p", action="store_true", help="start node agent poller")
    parser.add_argument("-c", action="store_true", help="start queue consumer")
    args = parser.parse_args()
    node_name = args.n
    na = NodeAgent(node_name)
    if args.p:
        na.start_poller()
    if args.c:
        na.start_consumer()

