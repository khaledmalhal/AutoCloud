from settings import Settings
from messages import Messages

class CommandExec():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.msg = Messages()

    def parse_command(self, data: dict):
        keys = data.keys()
        if 'edgedevice' in keys and 'command' in keys and 'message' in keys:
            command = data['command']
            msg = data['message']
            return command, msg

    def execute(self, data: dict):
        command, msg = self.parse_command(data)
        if command == self.msg.COMMAND_PRINT:
            print(f'Message from Cloud: {msg}')
            return True