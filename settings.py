import os
from dotenv import load_dotenv

class Settings():
    def __init__(self):
        load_dotenv()
        self._im_edge = eval(os.getenv("EDGE"))
        self._name    = os.getenv('NAME')
        self._api_url = os.getenv('API_URL')
        
        self._influx_bucket  = os.getenv("INFLUX_BUCKET")
        self._influx_token   = os.getenv("INFLUX_TOKEN")
        self._influx_org     = os.getenv("INFLUX_ORG")
        self._influx_url     = os.getenv("INFLUX_URL")

        self._dns_ip   = os.getenv('DNS_IP')
        self._dns_port = os.getenv('DNS_PORT')

        self._success = not (self._im_edge == None or self._name == None or self._api_url == None or
                        self._influx_bucket == None or self._influx_token == None or 
                        self._influx_org == None or self._influx_url == None)
        if self._success is False:
            raise Exception(
            """
            The .env file is incomplete. Make sure to add the following properties:
                NAME:          Name of the device.
                EDGE:          True or False. If it is an Edge Device, set this up as True.
                API_URL:       The API_URL that provides the necessary API.
                INFLUX_BUCKET: The Bucket string of the InfluxDB.
                INFLUX_TOKEN:  The necessary token to access to the InfluxDB
                INFLUX_ORG:    The organization for the InfluxDB
                INFLUX_URL:    The URL of where the InfluxDB is hosted. You should also include the port if necessary.
            """
            )
    def get_im_edge(self):
        return self._im_edge
    def set_im_edge(self, value):
        if self._im_edge != value:
            self._im_edge = value

    def get_name(self):
        return self._name
    def set_name(self, value):
        if self._name != value:
            self._name = value

    def get_api_url(self):
        return self._api_url
    def set_api_url(self, value):
        if self._api_url != value:
            self._api_url = value

    def get_influx_bucket(self):
        return self._influx_bucket
    def set_influx_bucket(self, value):
        if self._influx_bucket != value:
            self._influx_bucket = value

    def get_influx_token(self):
        return self._influx_token
    def set_influx_token(self, value):
        if self._influx_token != value:
            self._influx_token = value

    def get_influx_org(self):
        return self._influx_org
    def set_influx_org(self, value):
        if self._influx_org != value:
            self._influx_org = value

    def get_influx_url(self):
        return self._influx_url
    def set_influx_url(self, value):
        if self._influx_url != value:
            self._influx_url = value

    def get_dns_ip(self):
        return self._dns_ip
    def set_dns_ip(self, value):
        if self._dns_ip != value:
            self._dns_ip = value

    def get_dns_port(self):
        return self._dns_port
    def set_dns_port(self, value):
        if self._dns_port != value:
            self._dns_port = value

    im_edge       = property(get_im_edge, set_im_edge)
    name          = property(get_name, set_name)
    api_url       = property(get_api_url, set_api_url)
    influx_bucket = property(get_influx_bucket, set_influx_bucket)
    influx_org    = property(get_influx_org, set_influx_org)
    influx_token  = property(get_influx_token, set_influx_token)
    influx_url    = property(get_influx_url, set_influx_url)
    dns_ip        = property(get_dns_ip, set_dns_ip)
    dns_port      = property(get_dns_port, set_dns_port)

    def to_dict(self) -> dict:
        return {
            'im_edge': self.im_edge,
            'name':    self.name,
            'api_url': self.api_url,
            'influx_bucket': self.influx_bucket,
            'influx_token':  self.influx_token,
            'influx_org':    self.influx_org,
            'influx_url':    self.influx_url,
            'dns_ip':   self.dns_ip,
            'dns_port': self.dns_port
        }

    def get_properties(self):
        return [p for p in dir(Settings) if isinstance(getattr(Settings,p),property)]
