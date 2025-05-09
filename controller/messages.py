import json

class Messages():
    def __init__(self, name='no_controller'):
        self.discovery = str({
            'type': 'discovery',
            'controller': name
        })