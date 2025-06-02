import requests
from settings import Settings

class EdgeDevices():
    """
    self.edge_devices is a list of dictionaries that contains a list of
    edge devices that are propertiary of this Controller.

    The template of the object dictionary is the following:
    {
        "controller": "laptop",
        "name": "autocloud1",
        "is_mobile": true,
        "longitude": 1.701044,
        "is_active": true,
        "latitude": 41.217968,
        "updated": true
    }
    All of the properties expect `updated` are the same as in the CloudDB.
    Update this class description accordingly, as it might change in the future.

    The property `updated` is simply to know when to update the property `is_active`.
    If the method `update_edge` has been called to activate the Edge Device once, then
    let's try not to call it many times for each pinging.
    """
    def __init__(self, settings: Settings):
        self.settings = settings
        self.name = settings.get_name()
        self.api_url = settings.get_api_url()
        self.edge_devices = []
        self.fetch_controllers_edge()
        print(f"Obtained the following edge devices for this controller: {[ edge['name'] for edge in self.edge_devices ]}")

    def fetch_controllers_edge(self):
        ret = requests.get(f'{self.api_url}/controller/{self.name}')
        try:
            if ret.ok:
                data = ret.json()
                if len(data['edgedevices']) == 0:
                    return
                self.edge_devices = [edge for edge in data['edgedevices']]
        except Exception as e:
            print(f"Error obtaining Edge Devices: {e}")

    def fetch_edge_device(self, edge: str):
        ret = requests.get(f'{self.api_url}/edge/{edge}')
        try:
            if ret.ok:
                data = ret.json()
                return data
        except Exception as e:
            print(f'Error updating edge: {e}')
            return None

    def link_edge(self, edge: str):
        ret = requests.post(f'{self.api_url}/controller/{self.name}/{edge}')
        try:
            if ret.ok:
                return True
        except Exception as e:
            print(f'Error updating edge: {e}')
            return False

    def update_edge(self, edge: str, data: dict):
        print(f'Updating {edge} with {data}')
        ret = requests.patch(f'{self.api_url}/edge/{edge}', json=data)
        try:
            if ret.ok:
                return True
        except Exception as e:
            print(f'Error at updating Edge Device {edge}')
        return False

    def unlink_edge(self, edge: str):
        ret = requests.delete(f'{self.api_url}/controller/{edge}')
        try:
            if ret.ok:
                device = self.get_edge_in_list(edge)
                if device is not None and 'ip' in device.keys():
                    del device['ip']
                    del device['controller']
                return True
        except Exception as e:
            print(f'Error updating edge: {e}')
            return False

    def append_or_update(self, edge_name: str, ip: str):
        # First get it from the Controller's DB.
        edge_dict = self.get_edge_in_list(edge_name)
        if edge_dict is None:
            # If it is not in this Controller, then fetch it from the Cloud.
            edge_dict = self.fetch_edge_device(edge_name)
            if edge_dict is None:
                self.remove_edge(edge_name)
                raise Exception("The edge device is not registered in the system.")
            # Then append it to this Controller's list of Edge Devices.
            self.edge_devices.append(edge_dict)
        edge_dict['ip'] = ip
        edge_dict['controller'] = self.name
        self.link_edge(edge_name)
        print(edge_dict)
        if 'updated' not in edge_dict.keys():
            self.update_edge(edge_name, {'is_active': True})
        edge_dict['updated'] = True

    def remove_edge(self, edge: str):
        self.unlink_edge(edge)
        self.update_edge(edge, {'is_active': False})
        self.edge_devices[:] = [d for d in self.edge_devices if d['name'] != edge]

    def get_edge_in_list(self, edge: str):
        ret = next((e for e in self.edge_devices if e['name'] == edge), None)
        return ret

    def get_edge_devices(self):
        return self.edge_devices