from collections import Counter
from util.db import db
import datetime

class NodeHealth:
    def healthCheck(self):
        nodeDetails = db.node_config.find()
        ## filter nodes if heart beat wasn't updated for more than 20 seconds
        failedNodes = [ node['name'] for node in nodeDetails 
                if ((datetime.datetime.utcnow() - node['heart_beat_time']).total_seconds() > 20) ]
        return failedNodes

    def updateContainer(self, failedNodes):
        records = db.container_config.update_many(
            {
                "$and": [
                    {
                        "node_mapping" : {
                            "$in": failedNodes
                        }
                    },
                    {
                        "state" : {
                            "$ne": "fail"
                        }
                    }
                ]
            },
            {
                "$set": {
                    "state": "fail"
                }
            }
        )
        if records:
            print('Total container records modified due to failed nodes are - ',str(records.modified_count))
            return records.modified_count
        else:
            print('Unable to modify container records for failed nodes')
            return 0

    def fetchServiceMapCount(self, failedNodes):
        records = db.container_config.find(
            {
                "$and": [
                    {
                        "node_mapping" : {
                            "$in": failedNodes
                        }
                    },
                    {
                        "state" : {
                            "$ne": "fail"
                        }
                    }
                ]
            }
        )
        serviceNames = [record['service_map'] for record in records]
        return Counter(serviceNames)

    def updateServiceReplicas(self, serviceCountMap):
        serviceNames = list(serviceCountMap.keys())
        serviceData = db.service_config.find(
            {
                "name" : {
                    "$in": serviceNames
                }
            }
        )
        
        ## bulk update logic (limited to 100 records per update)
        bulkServiceUpdate = db.service_config.initialize_unordered_bulk_op()
        counter = 0
        for data in serviceData:
            val = data['current_state'] - serviceCountMap[data['name']]
            if val < 0:
                val = 0
            bulkServiceUpdate.find(
                    {
                        "_id": data['_id']
                    }
                ).update(
                    {
                        "$set": { 
                            "current_state": val
                        }
                    }
                )
            counter += 1
            if (counter % 100 == 0):
                bulkServiceUpdate.execute()
                bulkServiceUpdate = db.service_config.initialize_unordered_bulk_op()

        if (counter % 100 != 0):
                bulkServiceUpdate.execute()
        

    ### Use only for testing
    def insertNodesOneTime(self):
        nodeList = []
        print(db.list_collection_names())
        for i in range(5):
            node = {}
            node['name'] = 'node'+str(i)
            node['description'] = 'Node '+str(i)
            node['heart_beat_time'] = datetime.datetime.utcnow()
            node['free_mem'] = 2.1+i
            node['free_cpu'] = 0.5+i
            node['free_disk'] = 500+i
            nodeList.append(node)
        output = db.node_config.insert_many(nodeList)
        print('Inserted are - ', output)

    @staticmethod
    ## update any node for testing
    def updateNodes(nodes):
        output = db.node_config.update_many(
            {
                "name" : {
                    "$in": nodes
                }     
            },
            {
                "$set": {
                    "heart_beat_time": datetime.datetime.utcnow()
                }
            }
        )
        print('Updated are - ', output.raw_result)




