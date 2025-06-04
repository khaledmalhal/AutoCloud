import uuid

class Messages():
    # Literals
    DISCOVERY        = "discovery"
    DISCOVERY_REPLY  = "discovery_reply"
    SENSOR_DATA      = "sensor_data"
    CLOUD_PING       = "cloud_ping"
    CLOUD_PING_REPLY = "cloud_ping_reply"
    COMMAND_EDGE     = "command_edge"

    COMMAND_PRINT    = "command_print"
    COMMAND_REPLY    = "command_reply"
    COMMAND_RUN_CAR  = "command_run_car"
    COMMAND_STOP_CAR = "command_stop_car"

    PENDING_STATUS   = "pending"
    SUCCESS_STATUS   = "success"
    FAILED_STATUS    = "failed"

    def __init__(self):
        pass

    def discovery(self, name: str):
        return str({
            "type": self.DISCOVERY,
            "controller": name
        }).encode('utf-8')

    def discovery_reply(self, name: str):
        return str({
            "type": self.DISCOVERY_REPLY,
            "edgedevice": name
        }).encode('utf-8')

    def sensor_data(self, key: str, value: str, edgedevice: str):
        return str({
            "type": self.SENSOR_DATA,
            "key": key,
            "value": value,
            "edgedevice": edgedevice
        }).encode('utf-8')

    def cloud_ping(self):
        return str({
            "type": self.CLOUD_PING
        }).encode('utf-8')

    def cloud_ping_reply(self):
        return str({
            "type": self.CLOUD_PING_REPLY
        }).encode('utf-8')

    def command_edge(self, edge: str, command: str, msg: str):
        return {
            "id": uuid.uuid1().bytes,
            "type": self.COMMAND_EDGE,
            "edgedevice": edge,
            "command": command,
            "message": msg,
            "status": self.PENDING_STATUS
        }

    def command_reply(self, edge: str, id: str, status: str):
        return str({
            "id": id,
            "type": self.COMMAND_REPLY,
            "edgedevice": edge,
            "status": status
        }).encode('utf-8')
