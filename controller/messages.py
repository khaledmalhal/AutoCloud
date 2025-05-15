import json

class Messages():
    # Literals
    DISCOVERY       = "discovery"
    DISCOVERY_REPLY = "discovery_reply"

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