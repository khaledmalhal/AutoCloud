import json

class Messages():
    # Literals
    DISCOVERY        = "discovery"
    DISCOVERY_REPLY  = "discovery_reply"
    SENSOR_DATA      = "sensor_data"
    CLOUD_PING       = "cloud_ping"
    CLOUD_PING_REPLY = "cloud_ping_reply"
    COMMAND_EDGE     = "command_edge"

    COMMAND_PRINT    = "command_print"

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

    def cloud_ping(self, name: str):
        return str({
            "type": self.CLOUD_PING,
            "controller": name
        }).encode('utf-8')

    def cloud_ping_reply(self):
        return str({
            "type": self.CLOUD_PING_REPLY
        }).encode('utf-8')

    def print_command(self, edge: str, command: str, msg: str):
        return str({
            "type": self.COMMAND_EDGE,
            "edgedevice": edge,
            "command": command,
            "message": msg
        }).encode('utf-u')