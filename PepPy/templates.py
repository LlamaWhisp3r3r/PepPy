class BaseTemplate:

    def __setitem__(self, key, value):
        self.params[key] = value

    def __getitem__(self, key):
        return self.params[key]

    def __str__(self):
        return str(self.params.items())

    def items(self):
        return self.params.items()

class EmailSettings(BaseTemplate):

    def __init__(self, host, security, port, sender, recipients, username=None, password=None, enable=True):
        """ Email Settings holder for peplink API

        Args:
            host (str): SMTP Server to use for sending email notifications
            security (str or None): Security to use for sending emails. Can be None, starttls, or ssltls
            port (int): Port for the SMTP (or host) server to use
            username (str): The username to login into SMTP server. This is not always required. Defaults to None
            password (str): The password to login into SMTP server. This is not always required. Defaults to None
            sender (str): The sender email address
            recipients (list): A list of recipients to send the notifications to
            enable (bool, optional): Enable and Disable email notifications. Defaults to True.
        """
        
        self.params = {
            'enable': enable,
            'host': host,
            'security': security,
            'port': port,
            'authentication': None,
            'sender': sender,
            'recipient': recipients,
            'func': 'config.notify'
        }

        if username:
            self.params['authentication'] = {
                'user': username,
                'password': password
            }

class TimeSettings(BaseTemplate):

    def __init__(self, timeZone, syncSource='server', timeServer='0.peplink.pool.ntp.org'):
        """ Time Settings holder for peplink API

        Args:
            timeZone (str): See this link to find all the different timezones that can be used
            syncSource (str, optional): Determines how the device will sync it's time. Defaults to 'server'
            timeServer (str, optional): Specify any ntp server that. Defaults to '0.peplink.pool.ntp.org'
        """
        
        self.params = locals()
        self.params['func'] = 'config.time'
        del self.params['self']

class AdminSettings(BaseTemplate):

    def __init__(self, name, admin_name=None, admin_password=None, user_name=None, user_password=None, web_session_timeout=14400, access_protocol_method='http+https',
                    http_redirect_to_https='yes', http_port=80, http_access='lan', https_port=443, https_access='lan'):
        """ Admin Settings data holder for Peplink API

        Args:
            name (str): Name of Peplink device
            admin_name (str, optional): Admin login username. Defaults to None.
            admin_password (str, optional): Admin login password. Defaults to None.
            user_name (str, optional): User login username. Defaults to None.
            user_password (str, optional): User login password. Defaults to None.
            web_session_timeout (int, optional): Web session timeout in seconds. Defaults to 14400.
            access_protocol_method (str, optional): Protocol used to access device. Can be http, https, or http+https. Defaults to 'http+https'.
            http_redirect_to_https (str, optional): If http redirects to https. Can be yes or no. Defaults to 'yes'.
            http_port (int, optional): HTTP port used by device. Only takes effect if access_protocol_method=http. Defaults to 80.
            http_access (str, optional): Where the Web Interface can be accessed from using HTTP. Can be lan or lan+wan. Defaults to 'lan'.
            https_port (int, optional): HTTPS port used by device. Only takes effect if access_protocol_method=https. Defaults to 443.
            https_access (str, optional): Where the Web Interface can be accessed from using HTTPS. Can be lan or lan+wan. Defaults to 'lan'.
        """

        self.arguments = locals()
        self.__set_parameters()

    def __set_parameters(self):
        self.params = {
            'device_name': self.arguments['name'],
            'name': self.arguments['name'],
            'legacy': '', # This needs to be here to make the request work
            'func': 'config.admin',
            'adminLoginName': self.arguments['admin_name'],
            'adminLoginPassword': self.arguments['admin_password'],
            'adminLoginPasswordConfirm': self.arguments['admin_password'],
            'userLoginName': self.arguments['user_name'],
            'userLoginPassword': self.arguments['user_password'],
            'userLoginPasswordConfirm': self.arguments['user_password'],
            'timeout': self.arguments['web_session_timeout'],
            'accessProtocol_method': self.arguments['access_protocol_method'],
            'accessProtocol_redirect': self.arguments['http_redirect_to_https'],
            'accessProtocol_http_port': self.arguments['http_port'],
            'accessProtocol_http_access': self.arguments['http_access'],
            'accessProtocol_https_port': self.arguments['https_port'],
            'accessProtocol_https_access': self.arguments['https_access']
        }

class PortForwarding(BaseTemplate):

    def __init__(self, name, server_ip_address, id=0, enable=True, protocol='TCP', external_port=None, mapped_port=None, allow_pepvpn=False,
                    enable_wan=False, enable_cell=False, enable_wifi_2=False, enable_wifi_5=False):
        """ Port Forwarding data holder for Peplink API

        Args:
            name (str): Name of port forwarding rule
            server_ip_address (str): Internal IP Address to forward the traffic to
            id (int, optional): Port forwarding id. Leave this at 0 for creating new port forwarding rules. Defaults to 0.
            enable (bool, optional): If the port forwarding rule is enabled or disabled. Defaults to True.
            protocol (str, optional): The protocol to use. Can be TCP, UDP, ICMP, or IP. Defaults to 'TCP'.
            external_port (int, optional): The external port to forward the taffic to. Defaults to None.
            mapped_port (int, optional): The mapped port to the internal IP Address. Defaults to None.
            allow_pepvpn (bool, optional): Enable or disable_pepvpn. Defaults to False.
            enable_wan (bool, optional): Enable the wan connection to pass this port forwarding rule. Defaults to False.
            enable_cell (bool, optional): Enable the cellular connection to pass this port forwarding rule. Defaults to False.
            enable_wifi_2 (bool, optional): Enable the 2.4 GHz Wi-Fi to pass this port forwarding rule. Defaults to False.
            enable_wifi_5 (bool, optional): Enable the 5 GHz Wi-Fi to pass this port forwarding rule. Defaults to False.
        """

        arguments = locals()
        self.params = {
            'func': 'config.inbound.service',
            'action': 'add',
            'list': [
                {
                    'id': id,
                    'enable': enable,
                    'name': name,
                    'protocol': {
                        'type': protocol,
                        'port': external_port,
                        'portMapper': mapped_port
                    },
                    'allowPepvpnConnection': allow_pepvpn,
                    'inboundServer': {
                        'action': 'add',
                        'ip': server_ip_address,
                        'name': ''
                    }
                }
            ]
        }
        self.__check_parameters(arguments)

    def __check_parameters(self, parameters):
        wan_connection = dict()
        order = list()
        if parameters['enable_wan']:
            wan_connection['1'] = {'ip': ['default']}
            order.append(1)
        if parameters['enable_cell']:
            wan_connection['2'] = {'ip': ['default']}
            order.append(2)
        if parameters['enable_wifi_2']:
            wan_connection['3'] = {'ip': ['default']}
            order.append(3)
        if parameters['enable_wifi_5']:
            wan_connection['4'] = {'ip': ['default']}
            order.append(4)
        
        if len(order) == 0:
            raise SyntaxError("Please enable one of these WAN connections (enable_wan, enable_cell, enable_wifi_2_4, enable_wifi_5).")

        wan_connection['order'] = order
        self.params['wanConnection'] = wan_connection

class GenericLan(BaseTemplate):

    def __init__(self, proxy_dns_enable='yes', proxy_dns_caching='no', proxy_google_dns='yes'):
        """ Generic Lan data holder for Peplink API

        Args:
            proxy_dns_enable (str, optional): Enable proxy DNS. Can be yes or no. Defaults to 'yes'
            proxy_dns_caching (str, optional): Enable DNS caching. Can be yes or no. Defaults to 'no
            proxy_google_dns (str, optional): Enable the use of Google's public DNS servers for proxy DNS. Can be yes or no. Defaults to 'no'
        """
                    
        self.params = {
            'section': 'LAN_generic_modify',
            'ldns_enable': proxy_dns_enable,
            'ldns_cache': proxy_dns_caching,
            'ldns_use_google': proxy_google_dns
        }

class LanProfile(BaseTemplate):

    def __init__(self, name, id=0, enable_dhcp=True, router_ip='192.168.50.1', router_subnet_mask=24, dhcp_pool_start='192.168.50.10', dhcp_pool_end='192.168.50.250',
                    dhcp_pool_subnet_mask='24', dhcp_lease_time=86400):
        """ Lan Profile data holder for Peplink API

        Args:
            name (str): Name of lan profile
            id (int, optional): Id of lan profile. This is only applicable if you have more than 1 lan profile. Defaults to 0.
            enable_dhcp (bool, optional): Enable dhcp mode. Defaults to True.
            router_ip (str, optional): Router IP Address. Defaults to '192.168.50.1'.
            router_subnet_mask (int, optional): Router subnet mask. Defaults to 24.
            dhcp_pool_start (str, optional): Dhcp pool starting IP Address. This is only applicable if dhcp is enabled. Defaults to '192.168.50.10'.
            dhcp_pool_end (str, optional): Dhcp pool ending IP Address. Defaults to '192.168.50.250'.
            dhcp_pool_subnet_mask (str, optional): Dhcp pool subnet mask. This is only applicable if dhcp is enabled. Defaults to '24'.
            dhcp_lease_time (int, optional): Dhcp lease time for IP Addresses. This is only applicable if dhcp is enabled. Defaults to 86400.
        """

        self.params = {
            'lan_id': id,
            'section': 'LAN_network_modify',
            'lan_ip': router_ip,
            'lan_mask': router_subnet_mask,
            'lan_name': name,
            'lan_dhcp_pool_start': dhcp_pool_start,
            'lan_dhcp_pool_end': dhcp_pool_end,
            'lan_dhcp_pool_mask': dhcp_pool_subnet_mask,
            'lan_dhcp_lease': dhcp_lease_time
        }

        if enable_dhcp:
            self.params['lan_dhcp_mode'] = 'server'
        else:
            self.params['lan_dhcp_mode'] = 'disable'

class CellularSettings(BaseTemplate):

    def __init__(self, instant_active=True, id=2, name='Cellular', enable=True, enable_healthcheck=True, enable_ddns=False,
                    schedule=None, cellular={'preferredSim': None, 'simCardScheme': '1'}, sim1_info=None, sim2_info=None, signal_level=0, priority=1, mtu=1342):
        """ Cellular Settings data holder for Peplink API

        Args:
            instant_active (bool, optional): Instant active cell card. Defaults to True.
            id (int, optional): The id of the wan connection. Cellular setting is always 2. Defaults to 2.
            name (str, optional): Name of Cellular setting. Defaults to 'Cellular'.
            enable (bool, optional): Enable Cell Settings. Defaults to True.
            enable_healthcheck (bool, optional): Enable healthcheck. Defaults to True.
            enable_ddns (bool, optional): Enable ddns. Defaults to False.
            schedule (dict, optional): Schedule for cell settings. Defaults to None.
            cellular (dict, optional): Set preferred sim and sim card scheme. Defaults to {'preferredSim': None, 'simCardScheme': '1'}.
            sim1_info (dict, optional): Collection of Sim information. Defaults to None.
            sim2_info (dict, optional): Collection of Sim information. Defaults to None.
            signal_level (int, optional): Singal level for cellular signal. Defaults to 0.
            priority (int, optional): The priority compared to other active wan connections. Defaults to 1.
            mtu (int, optional): The maxium transmit unit. Firstnet is 1342. Defaults to 1342.
        """

        # Sim Information has to be filled out for request to be sucessfull
        if not sim1_info:
            sim1_info = {
                'id': 1,
                'carrierSelection': None,
                'mobileType': None,
                'bandSelection': None,
                'roaming': {
                    'enable': False
                },
                'authentication': None,
                'operator': None,
                'simPin': None,
                'bandwidthAllowanceMonitor': {
                    'enable': False
                }
            }
        if not sim2_info:
            sim2_info = {
                'id': 2,
                'carrierSelection': None,
                'mobileType': None,
                'bandSelection': None,
                'roaming': {
                    'enable': False
                },
                'authentication': None,
                'operator': None,
                'simPin': None,
                'bandwidthAllowanceMonitor': {
                    'enable': False
                }
            }

        cellular['sim'] = [sim1_info, sim2_info]
        cellular['signalThreshold'] = {'signalLevel': [signal_level]}
        connection = {
            'groupSet': 0,
            'icmpPing': True,
            'hotStandby': {
                'enable': True,
                'schedule': None
            },
            'idleTimeout': None,
            'priority': priority,
            'method': {
                'type': 'dhcp',
                'detail': {
                    'ipPassthrough': False,
                    'staticRoute': None,
                    'hostname': ""
                }
            },
            'routingMode': 'NAT',
            'dns': {
                'auto': True,
                'host': []
            },
            'cellularModule': {
                'networkMode': ""
            }
        }
        new_ddns = {'enable': enable_ddns}
        new_healthcheck = {
            'enable': enable_healthcheck,
            'method': {
                'type': 'smartcheck',
                'detail': {'host': []}
            },
            'timeout': 5000,
            'interval': 10,
            'retry': 3,
            'recovery': 3
        }

        self.params = {
            'func': 'config.wan.connection',
            'agent': 'webui',
            'action': 'update',
            'instantActive': instant_active,
            'list': [
                {
                    'id': id,
                    'name': name,
                    'enable': enable,
                    'healthcheck': new_healthcheck,
                    'ddns': new_ddns,
                    'schedule': schedule,
                    'cellular': cellular,
                    'connection': connection,
                    'physical': {
                        'mtu': mtu,
                        'ttl': None,
                        'poe': {
                            'enable': False,
                            'schedule': None
                        }
                    }
                }
            ],
            'enforce': False
        }
