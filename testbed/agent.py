"""Agent

This script implements the `Agent` abstract class. It inherits from
the communication interface class to communicate between agents.

"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

from comminterface import *
import time

from _thread import *


class Route:
    __route = []
    __actions = []

    def __init__(self, route=[]):
        if len(route) > 0:
            self.__route = route
            print('INITIAL ROUTE: ' + str(self.__route))
            self.set_actions(self.__route)
        else:
            self.__set_default_route()

    def compute_actions(self, route):
        actions_list = []

        for index, source in enumerate(route):
            try:
                if index + 1 < len(route):
                    target = route[index + 1]
                    actions = routing_table.get((source, target))
                    if actions is not None:
                        a = {'source': source, 'target': target, 'actions': actions}
                        actions_list.append(a)
            except Exception as e:
                print(e)
        return actions_list

    def compute_route(self, source, target):
        pass

    def __compute_default_route(self):
        route = []
        '''
        route.append(RFIDTAG.SW)
        route.append(RFIDTAG.W4)

        route.append(RFIDTAG.NW)
        route.append(RFIDTAG.NW)

        route.append(RFIDTAG.SW)
        route.append(RFIDTAG.W4)
        route.append(RFIDTAG.W3)
        route.append(RFIDTAG.W2)
        route.append(RFIDTAG.W1)
        route.append(RFIDTAG.N1)
        route.append(RFIDTAG.N2)
        #route.append(RFIDTAG.N2)
        route.append(RFIDTAG.SW)
        route.append(RFIDTAG.SW)
        '''
        #...
        '''
        route.append(RFIDTAG.SW)
        route.append(RFIDTAG.W4)
        route.append(RFIDTAG.W3)
        route.append(RFIDTAG.W2)
        route.append(RFIDTAG.W1)
        route.append(RFIDTAG.NW)
        route.append(RFIDTAG.NW)
        '''

        return route

    def set_route(self, route):
        self.__route.clear()
        self.__route = route
        print('ROUTE UPDATED: ' + str(self.__route))
        self.set_actions(self.__route)


    def set_actions(self, route):
        self.__actions.clear()
        self.__actions = self.compute_actions(route)
        print('ACTIONS UPDATED: ' + str(self.__actions))

    def __set_default_route(self):
        self.__route.clear()
        self.__route = self.__compute_default_route()
        print('DEFAULT ROUTE: ' + str(self.__route))
        self.set_actions(self.__route)

    def pop_next_actions(self):
        try:
            if self.has_actions():
                actions = self.__actions.pop(0)
                source = actions.get('source')
                target = actions.get('target')
                actions = actions.get('actions')
                return source, target, actions
        except Exception as e:
            print("pop_next_actions {}".format(e))
        print("There are no pending actions")
        return '', '', ''

    def has_actions(self):
        if len(self.__actions) > 0:
            return True
        return False

    def print_route(self):
        if len(self.__route)>0:
            print('\nROUTE: ' + str(self.__route))
        else:
            print('\nNO ROUTE')
        #print('\nPENDING ACTIONS: ' + str(self.__actions) + '\n')



class Agent(API):
    """
    An abstract class used to represent an Agent. It inherits from the `API`
    class to facilitate communication between agents.

    ...

    Attributes
    ----------
    __description : str
        a string to provide agent's description
    __coordinates : str
        a string representing the agent's position (i.e., rfid tag id)
    ready : bool
        a boolean indicating whether the agent is ready or not (default True)

    Methods
    -------
    __print_constructor_message()
        Prints agent's data on construction.
    __runtime()
        It invokes to methods __run() and __run_default() and starts an
        infinite loop
    __run_default()
        It starts a new thread invoking method run_default()
    __run()
        It starts a new thread invoking method run()
    run_default()
        Abstract class to represent the default behaviour of the agent
    ** run() **
        Abstract class to represent the particular behaviour of the agent
        defined by the testbed user/developer/researcher
    set_coordinates(tagid)
        It sets the __coordinates to `tagid`
    get_coordinates()
        Gets the coordinates
    __is_ready()
        Returns if agent is ready or not
    is_ready()
        Returns if agent is ready or not
    __set_ready(b)
        It sets __ready to `b`
    set_ready(b)
        It sets __ready to `b`
    wait_ready(s=1)
        It checks if agent is ready. If it is not ready, it waits for `s`
        seconds to check again, until agent is ready.
    """

    '''
    __description = ""
    __coordinates = ""
    ready = True
    '''

    __digitaltwin_id = None
    __digitaltwin_enabled = False
    __destroy = False

    _route = []

    def destroy(self):
        self.__destroy = True
        #print(self.__destroy)

    def digitaltwin_is_enabled(self):
        return self.__digitaltwin_enabled

    def digitaltwin_enable(self):
        self.__digitaltwin_enabled=True

    def digitaltwin_disable(self):
        self.__digitaltwin_enabled=False

    def set_digitaltwin_id(self, id):
        self.__digitaltwin_id=id

    def get_digitaltwin_id(self):
        return self.__digitaltwin_id

    def __init__(self, hostname, ip, port, description: str = None, dns_ip=None, dns_port=None):
        print(ip)
        API.__init__(self, hostname, ip, port, dns_ip, dns_port)
        print("hola")
        self.__description = description
        self.__print_constructor_message()
        self.__runtime()

    def __print_constructor_message(self):
        """Prints agent's name, ip, port and description on construction."""
        print('New agent `' + self.get_hostname() + '` created with interface IP ' + self.get_ip() + ':' + str(
            self.get_port()) + '. Desc.: ' + self.__description)

    def __runtime(self):
        """It invokes to methods __run() and __run_default() to create two
        threads that will contain agents runtime code and starts an
        infinite loop."""
        print("'" + self.get_hostname() + "'" + ' running @' + self.get_ip() + ':' + str(self.get_port()) + ' ' + str(
            self.get_platform()))
        self.__run()
        self.__run_default()
        while not self.__destroy:
            pass

    def run_default(self):
        """Abstract class to represent the default behaviour of the agent."""
        pass

    def run(self):
        """Abstract class to represent the particular behaviour of the agent
        defined by the testbed user/developer/researcher."""
        pass

    def __run_default(self):
        """It starts a new thread invoking method run_default()

        """
        try:
            start_new_thread(self.run_default, ())
        except Exception as e:
            print("ERROR:{}".format(e))

    def __run(self):
        """It starts a new thread invoking method run().

        """
        try:
            start_new_thread(self.run, ())
        except Exception as e:
            print("ERROR:{}".format(e))

    def set_coordinates(self, tagid):
        """It sets the __coordinates to `tagid`.

        Parameters
        ----------
        tagid : str
           The rfid tag id to set to __coordinates.
        """
        self.__coordinates = tagid

    def get_coordinates(self):
        """Gets the coordinates.

        Returns
        -------
        str
            the value of __coordinates
        """
        return self.__coordinates

    def __is_ready(self):
        """Returns if agent is ready or not.

        Returns
        -------
        bool
            the value of ready
        """
        return self.ready

    def is_ready(self):
        """Returns if agent is ready or not.

        Returns
        -------
        bool
            the value of ready
        """
        return self.__is_ready()

    def __set_ready(self, b):
        """It sets __ready to `b`.

        Parameters
        ----------
        b : bool
           The boolean value to set to __coordinates.

        """
        self.ready = b
        if self.ready:
            print('Agent is ready')
        else:
            print('Agent is not ready')

    def set_ready(self, b):
        """It sets __ready to `b`.

        Parameters
        ----------
        b : bool
           The boolean value to set to __coordinates.

        """
        self.__set_ready(b)

    def wait_ready(self, s: float = 1):
        """It checks if agent is ready. If it is not ready, it waits for `s`
        seconds to check again, until agent is ready.

        Parameters
        ----------
        s : float
           The seconds to wait until checking again if agent is ready (default 1)
        """
        while not self.__is_ready():
            time.sleep(s)

    def print_route(self):
        try:
            print(self._route.print_route())
        except:
            print("No route defined for this agent.")
