import os
import signal
from settings import Settings
from controller.messages import Messages
from hardware.Line_Tracking import Line_Tracking

class CommandExec():
    def __init__(self, settings: Settings = None):
        self.settings = settings
        self.msg = Messages()
        self.line = Line_Tracking()
        self.running = False

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
            return True, ""
        elif command == self.msg.COMMAND_RUN_CAR or command == self.msg.COMMAND_STOP_CAR:
            return self.manage_car(command)

    def manage_car(self, command: str):
        if command == self.msg.COMMAND_RUN_CAR and self.running is True:
            return False, "The car is already running."
        if command == self.msg.COMMAND_STOP_CAR and self.running is False:
            return False, "The car is already stopped."

        if self.running is False:
            self.line_pid = os.fork()
            if self.line_pid:
                self.running = True
                return True, "The car is now running."
            else:
                while True:
                    self.line.run()
        else:
            # Send SIGINT to the line process to stop the car from running
            os.kill(self.line_pid, signal.SIGINT)
            self.running = False
            return True, "The car has been stopped."