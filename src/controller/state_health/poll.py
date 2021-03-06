from datetime import datetime
from state_health.state_poll import StateHealth
def desiredstate():
    poll_time = str(datetime.utcnow())
    print(poll_time,'Desired State Poller: Initiated')
    instance = StateHealth()
    ## Retrieve inconsistent services
    inconsistent_service_names, inconsistent_service_details = instance.desiredStateCheck()
    print(poll_time,'Desired State Poller: inconsistent services are ', inconsistent_service_names)
    if inconsistent_service_names:
        ## analyze the containers if any in 'queue' state for a long time, if so, fail them
        print(poll_time,'Desired State Poller: Analyzing containers in queue state......')
        #instance.analyzeContainerInQueueState(inconsistent_service_names)
        ## reach the desired state by invoking API server
        print(poll_time,'Desired State Poller: Trying to reach end state......')
        instance.constructDesiredState(inconsistent_service_names, inconsistent_service_details)
    print(poll_time,'Desired State Poller: Finished')