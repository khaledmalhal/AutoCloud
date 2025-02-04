"""Communication Interface

*** WORKS ONLY WITH PYTHON 3+ ***

It implements the `API` abstract class, on top of the project's
classes, and implements the communication interface between agents.

This file can also be imported as a module and contains the following
function:
    * message - returns a JSON formatted string

"""

__author__ = "A. Asensio, S. Sanchez"
__credits__ = ["Adrian Asensio", "Sergi Sanchez"]
__version__ = "1.0.1"
__status__ = "Development"

import json

from testbed import *

import datetime
import errno
import socket
import threading
import time
import distro

#from sc_layout import port_default
from _thread import *


def message(uid, source, target, action, args=[], content=None):
    """Returns JSON formatted string representing the data to send
    between comm. interfaces to notify events or request actions

    Parameters
    ----------
    uid : str
        The unique identifier of the source agent
    source : str
        The name of the source agent
    target : str
        The name of the target agent
    action : str
        The action to perform on the target agent
    args : list
        A list of strings representing the arguments to pass to the action
    content : Any, optional
        Not utilized / Not implemented

    Returns
    -------
    str:
        a JSON formatted string
    """
    dict = {
        "uid": uid,
        "source": source,
        "target": target,
        "action": action,
        "args": args,
        "content": content
    }

    json_object = json.dumps(dict, indent=4)
    return json_object


class API:
    """
    Abstract class to implement communication interfaces between agents in the testbed

    ...

    Attributes
    ----------
    __platform : tuple
        information about the current OS distribution as a tuple (id_name, version, codename)
        from distro.linux_distribution()
    __ubuntu : bool
        value True if host runs Ubuntu
    __darwin : bool
        value True if host runs Mac OS

    __ip : str
        comm. interface ip (i.e., agent's ip)
    __port : int
        comm. interface port (i.e., agent's port)
    __hostname
        Name of the host
    __dns_ip
        DNS' ip
    __dns_port : int
         DNS' port
    __print_lock : Object threading.Lock()
    __default_ip_range : str
        Not utilized; e.g., '10.0.' to force Zephyrus ips
    __notify_to : list
        list of hosts (hostnames) subscribed to the notifications of
        this comm. interface (agent)
    _route : RFIDTAG list
        list of RFIDTAGs representing the route to follow.
    _info : str
        Information to show on creation.
    _help : str
        Help to show on creation.

    Methods
    -------
    __threaded(c)
        Listens and waits to receive data from a socket. If data are received,
        they are forwarded to method __api and returns the corresponding response.
    __api(data)
        Parses and formats the data received into tuple <action, args[]> and sends
        it to the __api_runtime method.
    __api_runtine(action, args)
        It calls the api_runtime method to process the received <action, args[]>
    __api_processing_default(action, args)
        Default processing for top-level actions:
        * 'get_hostname'
        * 'get_ip'
        * 'get_port'
        * 'get_dns_ip'
        * 'get_dns_port'
        * 'is_dns'
        * 'get_coordinates'
        * 'quit'
        * 'args'
        * 'notify'
        * 'info'
        * 'help'
        * 'hello'
        * 'subscribe'
        * 'unsubscribe'
        * 'msg'
        * 'tsmsg'
        * 'mhelp'
        * 'print_route'
    __start_apiserver()
        Executes the API server
    __run_apiserver()
        Creates a new thread to launch the API server
    __find_dns(ip, port)
        Not utilized. Tries to find the agent acting as DNS.
    __api_send(host, message, port=None, retries=0)
        Method to send a message to an agent
    __print_timestamp(msg=None)
        Prints the current timestamp. If msg is given, it prints the current
        timestamp and msg
    __dns_get_ip(hostname)
        Asks to the DNS for the IP of the host given the hostname
    __dns_get_port(hostname)
        Asks to the DNS for the port of the host given the hostname
    __dns_get_hostname_by_ip_port(ip, port)
        Asks to the DNS for the name of the host given the ip and port
    __dns_get_hostname(ip)
        Not implemented
    __dns_insert(hostname, ip, port)
        Asks the DNS to register hostname to the ip ad port given
    __notify(message, target=__notify_to)
        Creates threads to notify message to each agent in target
        if provided (as list of strings) or to its current subscribers
        if target is not provided
    __send_notify(to, message)
        Sends notification (message) to an agent (to) and discards its response
    __get_info()
        Returns self.info
    __get_help()
        Returns self.help
    __set_notify_to(notify_to)
        Sets the list of subscribers
    __subscribe(name)
        Adds a subscriber
    __unsubscribe(name)
        Removes a subscriber

    ** api_processing(action, args) **
        Abstract. Processing of tuple <action, args[]> received according
        to particular behaviour of agent user/developer/researcher's design
        and functionalities
    api_processing_default(action, args)
        Abstract. Processing of tuple <action, args[]> received according
        to the default behaviour of a particular agent design and functionalities
    api_runtine(action, args)
        It processes the <action, args[]> received according to the following
        order until the action to carry on is defined and returns the response
        to the action:
        * api_processing(action, args)
        * api_processing_default(action, args)
        * __api_processing_default(action, args)
    api_send(host, message, port=None)
        Method to send a message to an agent. Public alias for __api_send
    execute_action(data)
    execute_actions_from_dict(actions)
    get_coordinates()
    get_dns_ip()
        Retuns the DNS' ip
    get_dns_port()
        Retuns the DNS' port
    get_help()
        Public alias for __get_help
    get_hostname()
        Returns self hostname
    get_info()
        Public alias for __get_info
    get_ip()
        Returns self ip
    get_platform()

    get_port()
        Returns self port
    has_subscribers()
        Returns True if it has subscribers; False otherwise
    message(uid, source, target, action, args=[], content=None)
        Calls to function message and returns JSON formatted string representing the data to send
        between comm. interfaces
    message_to_action_args(action, args)
    notify(action, args, target=[])
    print_timestamp(msg=None)
        Public alias for __print_timestamp
    set_dns_ip(ip)
    """

    '''
    __platform = distro.linux_distribution()
    __ubuntu: bool = False
    __darwin: bool = False
    __ip: str = None
    __port: int = port_default  # 12301
    __hostname: str = None
    __dns_ip: str = None
    __dns_port: int = None  # 12300  # 12300  # reserved for dns nodes
    __print_lock = threading.Lock()
    __default_ip_range: str = ''  # '10.0.'  #To force Zephyrus ips

    __notify_to: list = []  # Nodes to notify events

    _route: list = []

    _info: str = '(not provided)'
    _help: str = '(not provided)'
    '''

    __platform = distro.linux_distribution()
    __ubuntu = False
    __darwin = False
    __ip = None
    __port = port_default  # 12301
    __hostname = None
    __dns_ip = None
    __dns_port = None  # 12300  # 12300  # reserved for dns nodes
    __print_lock = threading.Lock()
    __default_ip_range = ''  # '10.0.'  #To force Zephyrus ips

    __notify_to = []  # Nodes to notify events

    #_route = []

    _info = '(not provided)'
    _help = '(not provided)'

    def __init__(self, hostname, ip, port, dns_ip: str=None, dns_port: int=None):
        """
        Parameters
        ----------
        hostname : str
            The host's name
        ip : str
            The host's ip. If ip is None, then it looks for the ip in the
            equipment/vm/container.
        port : int
            The port number to communicate with the agent. If port is the same
            as the dns_port and ip is None, then it looks for the ip in the
            equipment/vm/container where this code is running and sets dns_ip
            to that ip
        dns_ip :  str
            The dns' ip (default None)
        dns_port : str
            The dns' port number to communicate to it (default None)

        """

        self.__platform = distro.linux_distribution()

        if 'ubuntu' in self.__platform[0].lower():
            self.__ubuntu = True
        elif 'darwin' in self.__platform[0].lower():
            self.__darwin = True

        if hostname == "":
            print("Hostname missing...")
            exit()
        self.__hostname = hostname

        if dns_ip is not None:
            self.__dns_ip = dns_ip
        if dns_port is not None:
            self.__dns_port = dns_port

        if port is not None:
            self.__port = port

        if port == self.get_dns_port() and ip is None:
            if self.__ubuntu:
                for i in socket.gethostbyname_ex(socket.gethostname() + ".local")[-1]:
                    if i == '127.0.0.1' or i == '127.0.1.1':
                        continue
                    if not i.startswith(self.__default_ip_range):
                        continue
                    ip = i
                    break
            else:
                for i in socket.gethostbyname_ex(socket.gethostname())[-1]:
                    if i == '127.0.0.1' or i == '127.0.1.1':
                        continue
                    if not i.startswith(self.__default_ip_range):
                        continue
                    ip = i
                    break
            self.__dns_ip = ip
            self.set_dns_ip(ip)
        if ip is None:
            if self.__ubuntu:
                for i in socket.gethostbyname_ex(socket.gethostname() + ".local")[-1]:
                    if i == '127.0.0.1' or i == '127.0.1.1':
                        continue
                    if not i.startswith(self.__default_ip_range):
                        continue
                    self.__ip = i
                    break
            else:
                for i in socket.gethostbyname_ex(socket.gethostname())[-1]:
                    if i == '127.0.0.1' or i == '127.0.1.1':
                        continue
                    if not i.startswith(self.__default_ip_range):
                        continue
                    self.__ip = i
                    break
        else:
            self.__ip = ip

        print('info: ' + self.__get_info())
        print('help: ' + self.__get_help())
        # self.__find_dns(self.__ip, self.__port)
        self.__run_apiserver()
        self.__dns_insert(self.__hostname, self.__ip, self.__port)

    def __threaded(self, c):
        """Listens and waits to receive data from socket connection c. If data are received,
        they are forwarded to method __api and sends back the corresponding response.

        Parameters
        ----------
        c : socket
            The socket connection
        """
        try:
            while True:
                # data received from client
                data = c.recv(1024)
                if not data:
                    # lock released on exit
                    self.__print_lock.release()
                    break
                reply = self.__api(data.decode('utf8'))

                # send back reply to client
                c.send(str(reply).encode('utf8'))
            # connection closed
            c.close()
        except Exception as e:
            print(e)

    def execute_actions_from_dict(self, actions):
        """Executes a set of actions given in a dict.

        Parameters
        ----------
        actions : dict
            The dict containing the set of actions (and their arguments, if any) to carry on

        Example
        -------
        * self.execute_actions_from_dict({0:'msg:Hello World!', 1:'get_ip'})
        * self.execute_actions_from_dict({0:{"action": "msg", "args": ["Hello World!"]}, 1: {"action":"get_ip"}})
        """
        for key, data in actions.items():
            print(self.__api(data))

    def execute_action(self, data):
        """Executes an action given as a str.

        Parameters
        ----------
        data : str or dict
            The action (and its arguments, if any) to carry on

        Returns
        -------
        str, None, bool, list:
            The value returned after executing the action

        Example
        ------
        self.execute_action_from_string('msg:Hello World!')\r\n
        self.execute_action_from_string({"action": "msg", "args": ["Hello World!"]})
        """
        return self.__api(data)

    def __api(self, data):
        """Parses and formats the data received into tuple <action, args[]> and sends
        it to the __api_runtime method.

        Parameters
        ----------
        data : str or dict
            The data representing the action and arguments to carry on

        Returns
        ------
        str:
            the __api_runtime method returned value
        """

        if isinstance(data, dict):
            action = data['action']
            args = []
            if 'args' in data:
                args = data['args']
        elif data.startswith('{'):
            data = json.loads(data)
            action = data['action']
            args = []
            if 'args' in data:
                args = data['args']
        else:
            if not data.endswith(":"):
                data += ":"
            action_args = data.split(':')

            action = action_args[0]
            args = None
            if len(action_args) > 1:
                action_args[1] = str(action_args[1]).replace(', ', ',').replace(' ,', ',')
                args = action_args[1].split(',')

        print(self.__hostname + " -> Request received: " + self.message_to_action_args(action, args))
        return self.__api_runtime(action, args)

    def __api_runtime(self, action, args):
        """It calls the api_runtime method to process the received <action, args[]>.

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine represented by action

        Return
        ------
        str:
            The reply from api_runtime
        """
        return self.api_runtime(action, args)

    def api_runtime(self, action, args):
        """It processes the <action, args[]> received according to the following
        order until the action to carry on is defined and returns the reply to the
        action:

        * api_processing(action, args)
        * api_processing_default(action, args)
        * __api_processing_default(action, args)

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine represented by action

        Return
        ------
        str, None, bool, list:
            The response returned after processing the action
        """
        reply = self.api_processing(action, args)
        if reply is None:
            reply = self.api_processing_default(action, args)
        if reply is None:
            reply = self.__api_processing_default(action, args)
        return reply

    def __api_processing_default(self, action, args):
        """Default processing for top-level actions.

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine represented by action

        Return
        ------
        str, None, bool or list:
            The response returned after processing the action
        """
        try:
            if action == "get_hostname":
                return self.get_hostname()
            elif action == "get_ip":
                return self.get_ip()
            elif action == "get_port":
                return str(self.get_port())
            elif action == "get_dns_ip":
                return self.get_dns_ip()
            elif action == "get_dns_port":
                return str(self.get_dns_port())
            elif action == "is_dns":
                if self.__port == self.__dns_port:
                    return True
                else:
                    return False
            elif action == "get_coordinates":
                return self.get_coordinates()
            elif action == 'quit':
                return 'Not implemented in this version'
            elif action == 'args':
                print(args)
                return args
            elif action == 'notify':
                # if isinstance(args, str):
                #    args = ast.literal_eval(args)
                # print(args)
                action = args[0]
                target = self.__notify_to

                if len(args) >= 3:
                    target = args[2]

                if len(args) >= 2:
                    args = args[1]
                else:
                    args = []
                # self.__notify(action, args, target)
                self.__notify(self.message('', '', '', action, args), target)
                return 'notified'
            elif action == "info":
                return self.__get_info()
            elif action == "help":
                return self.__get_help()
            elif action == "hello":
                print('Hello!')
                return 'said hello'
            elif action == "subscribe":
                self.__subscribe(args[0])
                return MESSAGE.SUBSCRIBED.value
            elif action == "unsubscribe":
                return self.__unsubscribe(args[0])
            elif action == 'msg':
                print(args[0])
                return 'Message shown'
            elif action == 'tsmsg':
                self.print_timestamp(args[0])
                return 'Message shown'
            elif action == 'mhelp':
                mhelp(args[0])
                return 'Help shown'
            elif action == 'print_route':
                #print(self._route.print_route())
                self.print_route()
                return 'Route printed'
            return MESSAGE.ACTION_UNKNOWN.value

        except Exception as e:
            # return 'Undefined command/action. {}'.format(e)
            return MESSAGE.ACTION_UNKNOWN.value

    def print_route(self):
        print('No route defined')

    def api_processing_default(self, action, args):
        """Abstract. Processing of tuple <action, args[]> received according
        to the default behaviour of a particular agent design and functionalities.

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine identified by action

        Return
        ------
        str, None, bool, list:
            The response returned after processing the action
        """
        return None

    def api_processing(self, action, args):
        """Abstract. Processing of tuple <action, args[]> received according
        to particular behaviour of agent user's design and functionalities.

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine represented by action

        Return
        ------
        str:
            The response returned after processing the action
        """
        return None

    def __start_apiserver(self):
        """Executes the API server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.__ip, self.__port))
        print("socket binded to port", self.__port)

        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")

        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            c, addr = s.accept()

            # lock acquired by client
            self.__print_lock.acquire()
            # print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            start_new_thread(self.__threaded, (c,))
        s.close()

    def __run_apiserver(self):
        """Creates a new thread to launch the API server"""
        start_new_thread(self.__start_apiserver, ())
        # time.sleep(0.1)  # To avoid sending data to apiserver before socket is created

    def api_send(self, host, message, port=None):
        """Method to send a message to an agent. Public alias for __api_send

        Parameters
        ----------
        host : str
            Target host
        message : str
            Message to send to host
        port : int
            Target host's port number

        Returns
        -------
        str:
            Response received from target host to the message
        """
        return self.__api_send(host, message, port)

    def message_to_action_args(self, action, args):
        """Formats action and args into a str representing the call to action(args)

        Parameters
        ----------
        action : str
            The action to carry on
        args : list[str]
            String list representing the arguments passed to the subroutine represented by action

        Return
        ------
        str:
            The string representing the call to action(args)
        """
        if len(args) >= 1:
            return action + "(" + str(args) + ")"
        else:
            return action + "()"

    def __find_dns(self, ip: str, port: int):
        """Not utilized. Tries to find the agent acting as DNS."""
        # Check all ips on port 12350
        if self.__dns_port == port:
            pass
        elif self.__dns_ip is not None:
            pass
        elif ip is not None:
            self.__dns_ip = None
            dns_ip = ip.split('.')
            # print(dns_ip)
            while self.__dns_ip is None:
                if self.__dns_ip is None:
                    for host in range(1, 255):
                        ip_to_check = dns_ip[0] + '.' + dns_ip[1] + '.' + dns_ip[2] + '.' + str(host)
                        print(ip_to_check + ":" + str(self.__dns_port))
                        is_dns = False
                        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s = socket.socket()
                        s.settimeout(0.1)  # 1 second
                        try:
                            s.connect((ip_to_check, self.__dns_port))  # "random" IP address and port
                            is_dns = True
                        except socket.error as exc:
                            print("Caught exception socket.error : %s" % exc)
                        s.close()
                        if is_dns:
                            print('Is DNS!!!')
                            self.__dns_ip = ip_to_check
                            break
                if self.__dns_ip is None:
                    for host in range(1, 255):
                        ip_to_check = dns_ip[0] + '.' + dns_ip[1] + '.128.' + str(host)
                        print(ip_to_check + ":" + str(self.__dns_port))
                        is_dns = False
                        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s = socket.socket()
                        s.settimeout(0.1)  # 1 second
                        try:
                            s.connect((ip_to_check, self.__dns_port))  # "random" IP address and port
                            is_dns = True
                        except socket.error as exc:
                            print("Caught exception socket.error : %s" % exc)
                        s.close()
                        if is_dns:
                            print('Is DNS!!!')
                            self.__dns_ip = ip_to_check
                            break
        else:
            print("Error")
            exit()

    def __api_send(self, host, message, port=None, retries=0):
        """Method to send a message to an agent

        Parameters
        ----------
        host : str
        message : str
        port : int
        retries : int

        Return
        ------
        str:
            The response received from the remote host
        """
        ip = ''
        try:
            if "." not in host:
                if port is None:
                    port = int(self.__dns_get_port(host))
                ip = self.__dns_get_ip(host)
            else:
                ip = host

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # connect to server on local computer

            s.settimeout(5)

            s.connect((ip, port))

            # message sent to server
            s.send(message.encode('utf8'))
            # message received from server
            response = s.recv(1024)
            # print the received message
            # print('Response received:', response.decode('utf8'))

            # close the connection
            s.close()

            # decoded_response = response.decode("UTF-8")
            # decoded_response = ast.literal_eval(decoded_response)
            return response.decode('utf8')
            # return response
        except socket.error as se:
            if retries > 0:
                time.sleep(0.1)
                self.__api_send(host, message, port, retries - 1)

            err = se.args[0]
            print("SOCKET ERROR:{}".format(se))
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                print('No data available')
        except Exception as e:
            if retries > 0:
                time.sleep(0.1)
                self.__api_send(host, message, port, retries - 1)
            print("{}".format(e))

    def get_hostname(self):
        """Returns self hostname

        Return
        ------
        str:
            __hostname
        """
        return self.__hostname

    def get_ip(self):
        """Returns self ip

        Return
        ------
        str:
            __ip
        """
        return self.__ip

    def get_port(self):
        """Returns self port

        Return
        ------
        int:
            __port
        """
        return self.__port

    def get_dns_ip(self):
        """Returns DNS' ip

        Return
        ------
        str:
            __dns_ip
        """
        return self.__dns_ip

    def set_dns_ip(self, ip):
        """Sets DNS' ip

        Parameters
        ----------
        ip : str
            Represents the DNS' ip to set up
        """
        self.__dns_ip = ip

    def get_dns_port(self):
        """Returns DNS' port

        Return
        ------
        int:
            __dns_port
        """
        return self.__dns_port

    def get_platform(self):
        """Returns DNS' port

        Return
        ------
        tuple:
            Information about the current OS distribution as a tuple (id_name, version, codename)
            from distro.linux_distribution()
        """
        return self.__platform

    def get_coordinates(self):
        """Abstract method"""
        return None

    def print_timestamp(self, msg=None):
        """Public alias for __print_timestamp
        Prints current timestamp or timestamp + msg, if msg is not None

        Parameters
        ----------
        msg : str
            String to print (if any) jointly with timestamp (default None)
        """
        self.__print_timestamp(msg)

    def __print_timestamp(self, msg=None):
        """Prints current timestamp or timestamp + msg, if msg is not None

        Parameters
        ----------
        msg : str
            String to print (if any) jointly with timestamp (default None)
        """
        e = datetime.datetime.now()
        if msg is not None:
            print("{0}: {1}".format(e, str(msg)))
        else:
            print("{0}".format(e))

    def __dns_get_ip(self, hostname: str):
        return self.__api_send(self.__dns_ip, '__dns_get_ip:' + hostname + ',', self.__dns_port)

    def __dns_get_port(self, hostname: str):
        return self.__api_send(self.__dns_ip, '__dns_get_port:' + hostname + ',', self.__dns_port)

    def __dns_get_hostname_by_ip_port(self, ip: str, port: int):
        return self.__api_send(self.__dns_ip, '__dns_get_hostname_by_ip_port:' + ip + ',' + str(port) + ',',
                               self.__dns_port)

    def __dns_get_hostname(self, ip: str):
        pass

    def __dns_insert(self, hostname: str, ip: str, port: int):
        try:
            print('Connecting to DNS...')
            resp = self.__api_send(self.__dns_ip, '__dns_insert:' + hostname + ',' + ip + ',' + str(port) + ',',
                                   self.__dns_port, 2)
            if resp is None:
                print('Cannot connect to DNS@' + str(self.__dns_ip) + ":" + str(self.__dns_port))
            else:
                print(resp)
        except Exception as e:
            print("{}".format(e))

    # def __notify(self, action, args, target=__notify_to):
    def __notify(self, message: str, target=__notify_to):
        for to in target:
            to = parse_name(to)
            # start_new_thread(self.__send_notify, (to, action, arg_list))
            start_new_thread(self.__send_notify, (to, message))

    '''
    def __send_notify(self, to, action, args):
        self.__api_send(to, action + ":" + args)
    '''

    def __send_notify(self, to: str, message: str):
        self.__api_send(to, message)

    def __get_info(self):
        return self._info

    def __get_help(self):
        return self._help

    def get_help(self):
        """Returns value of __help. Public alias of __get_help()

        Return
        ------
        str:
            String __help
        """
        return self.__get_help()

    def get_info(self):
        """Returns value of __info. Public alias of __get_info()

        Return
        ------
        str:
            String __info
        """
        return self.__get_info()

    def __set_notify_to(self, notify_to):
        self.__notify_to = notify_to

    def __subscribe(self, name: str):
        self.__notify_to.append(name) if name not in self.__notify_to else self.__notify_to
        print('subscribers: ' + str(self.__notify_to))

    def __unsubscribe(self, name: str):
        try:
            self.__notify_to.remove(name)
            print('subscribers: ' + str(self.__notify_to))
            return MESSAGE.UNSUBSCRIBED.value
        except Exception as e:
            return 'Nothing to do. You were not subscribed.'

    def notify(self, action, args, target=__notify_to):
        """Sends notification (<action, args[]>) to agents (target) and discards its response

        Parameters
        ------
        action : str
            String representing the action to carry on
        args : list[str]
            String list representing the arguments passed to subroutine represented by action
        target : list[str]
            String list representing the traget hosts to send the notification. If not provided,
            notification is sent to hosts subscribed to it (in __notify_to list)
        """
        # self.__notify(action, args, target)
        self.__notify(self.message('', '', '', action, args), target)

    def has_subscribers(self):
        """Returns True if it has subscribers; False otherwise

        Return
        ------
        bool:
            True if it has subscribers (i.e., __notify_to has elements);
            False if it has no subscribers (i.e., __notify_to is empty);
        """
        if len(self.__notify_to) > 0:
            return True
        return False

    '''
    def dict_msg(self, uid, source, target, action, args=[], content=None):
        return dict_msg(uid, source, target, action, args, content)
    '''

    def message(self, uid, source, target, action, args=[], content=None):
        """Calls to function message and returns JSON formatted string representing the data to send
        between comm. interfaces

        Parameters
        ----------
        uid : str
        source : str
        target : str
        action : str
        args : list[str]
        content : Not utilized

        Returns
        -------
        str:
            The data to send encoded as a JSON fromatted string
        """
        return message(uid, source, target, action, args, content)
