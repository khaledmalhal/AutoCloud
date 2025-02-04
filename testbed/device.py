"""Device

This script implements the `Device` abstract class. It inherits from
the Agent class and represents either a physical or a virtual IoT-like
device in the testbed.

"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

from agent import *


class Device(Agent):
    """
    A class representing a testbed device

    ...

    Attributes
    ----------
    __virtual : bool
        a boolean defining if the device is virtual (True) or physical (False, default)

    Methods
    -------
    set_virtual(b)
        Sets the value of __virtual to boolean b
    is_virtual()
        Returns True if the device is virtual
    """

    __virtual = False

    def __init__(self, hostname, ip, port, description=None, dns_ip=None, dns_port=None):
        Agent.__init__(self, hostname, ip, port, description, dns_ip, dns_port)

    def is_virtual(self):
        """Indicates if a device is virtual or not.

        Returns
        -------
        bool
            True if device is virtual; False, otherwise.
        """
        return self.__virtual

    def set_virtual(self, b):
        """Sets the value of __virtual to boolean b.

        Parameters
        ----------
        b : bool
           True to set the device as virtual; False to set teh device as physical
        """
        self.__virtual = b