class Orchestrator:
    def submit_task(self, agent_id, payload):
        raise NotImplementedError

    def track_status(self, task_id):
        raise NotImplementedError

    def register_agent(self, agent_info):
        raise NotImplementedError

    def submit_workflow(self):
        raise NotImplementedError
