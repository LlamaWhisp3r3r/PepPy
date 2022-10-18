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

    def __init__(self, host, security, port, username, password, sender, recipients, enable=True):
        """ Email Settings holder for peplink API

        Args:
            host (str): _description_
            security (_type_): _description_
            port (int): _description_
            username (str): _description_
            password (str): _description_
            sender (str): _description_
            recipients (list): _description_
            enable (bool, optional): _description_. Defaults to True.
        """
        
        self.params = {
            'enable': enable,
            'host': host,
            'security': security,
            'port': port,
            'authentication': {
                'user': username,
                'password': password
            },
            'sender': sender,
            'recipient': recipients,
            'func': 'config.notify'
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

    def __init__(self, name, is_enforce=None, adminLoginName=None,
                    adminLoginPassword=None, userLoginName=None, userLoginPassword=None,
                    frontPanel_password=None, fp_pw_1=0, fp_pw_2=0, fp_pw_3=0, fp_pw_4=0, timeout=3600,
                    timeout_hh=1, timeout_mm=0, auth_method=None, tacacsplus_host=None, tacacsplus_secret=None, tacacsplus_timeout=3,
                    auth_protocol="MS-CHAP+v2", auth_timeout=None, coa_port=None, acct_interval=None, cli_access=None, cli_access_lanonly="yes",
                    cli_port=None, cli_loginGraceTime=None, accessProtocol_method="https", accessProtocol_redirect=None,
                    accessProtocol_http_port=None, accessProtocol_http_access=None, accessProtocol_https_port=443, accessProtocol_https_access="lan",
                    access_protocol="https", http_admin_access_lanonly="yes", https_admin_access_lanonly0="yes",
                    https_admin_access_lanonly="yes", http_port=None, https_port=443, lanAccess_custom="no", lanAccess_id=0,
                    wan_access_custom="no", wanAccess_sourceSubnets=None, soruce_subnets=None, conn_1="default", conn_2="default",
                    conn_3="default", conn_4="default"):
        """_summary_

        Args:
            name (_type_): _description_
            is_enforce (_type_, optional): _description_. Defaults to None.
            adminLoginName (_type_, optional): _description_. Defaults to None.
            adminLoginPassword (_type_, optional): _description_. Defaults to None.
            userLoginName (_type_, optional): _description_. Defaults to None.
            userLoginPassword (_type_, optional): _description_. Defaults to None.
            frontPanel_password (_type_, optional): _description_. Defaults to None.
            fp_pw_1 (int, optional): _description_. Defaults to 0.
            fp_pw_2 (int, optional): _description_. Defaults to 0.
            fp_pw_3 (int, optional): _description_. Defaults to 0.
            fp_pw_4 (int, optional): _description_. Defaults to 0.
            timeout (int, optional): _description_. Defaults to 3600.
            timeout_hh (int, optional): _description_. Defaults to 1.
            timeout_mm (int, optional): _description_. Defaults to 0.
            auth_method (_type_, optional): _description_. Defaults to None.
            tacacsplus_host (_type_, optional): _description_. Defaults to None.
            tacacsplus_secret (_type_, optional): _description_. Defaults to None.
            tacacsplus_timeout (int, optional): _description_. Defaults to 3.
            auth_protocol (str, optional): _description_. Defaults to "MS-CHAP+v2".
            auth_timeout (_type_, optional): _description_. Defaults to None.
            coa_port (_type_, optional): _description_. Defaults to None.
            acct_interval (_type_, optional): _description_. Defaults to None.
            cli_access (_type_, optional): _description_. Defaults to None.
            cli_access_lanonly (str, optional): _description_. Defaults to "yes".
            cli_port (_type_, optional): _description_. Defaults to None.
            cli_loginGraceTime (_type_, optional): _description_. Defaults to None.
            accessProtocol_method (str, optional): _description_. Defaults to "https".
            accessProtocol_redirect (_type_, optional): _description_. Defaults to None.
            accessProtocol_http_port (_type_, optional): _description_. Defaults to None.
            accessProtocol_http_access (_type_, optional): _description_. Defaults to None.
            accessProtocol_https_port (int, optional): _description_. Defaults to 443.
            accessProtocol_https_access (str, optional): _description_. Defaults to "lan".
            access_protocol (str, optional): _description_. Defaults to "https".
            http_admin_access_lanonly (str, optional): _description_. Defaults to "yes".
            https_admin_access_lanonly0 (str, optional): _description_. Defaults to "yes".
            https_admin_access_lanonly (str, optional): _description_. Defaults to "yes".
            http_port (_type_, optional): _description_. Defaults to None.
            https_port (int, optional): _description_. Defaults to 443.
            lanAccess_custom (str, optional): _description_. Defaults to "no".
            lanAccess_id (int, optional): _description_. Defaults to 0.
            wan_access_custom (str, optional): _description_. Defaults to "no".
            wanAccess_sourceSubnets (_type_, optional): _description_. Defaults to None.
            soruce_subnets (_type_, optional): _description_. Defaults to None.
            conn_1 (str, optional): _description_. Defaults to "default".
            conn_2 (str, optional): _description_. Defaults to "default".
            conn_3 (str, optional): _description_. Defaults to "default".
            conn_4 (str, optional): _description_. Defaults to "default".
        """
        
        self.params = locals()
        self.params['device_name'] = name
        self.params['legacy'] = '' # This needs to be here to make the request work
        self.params['func'] = 'config.admin'
        del self.params['self']
        self.__check_parameters()

    def __check_parameters(self):
        if self.params['adminLoginPassword']:
            self.params['adminLoginPasswordConfirm'] = self.params['adminLoginPassword']
        
        if self.params['userLoginPassword']:
            self.params['userLoginPasswordConfirm'] = self.params['userLoginPassword']

class PortForwarding(BaseTemplate):

    def __init__(self, name, server_ip_address, id=0, enable=True, protocol=("TCP", 554, None), allow_pepvpn=False,
                    wan_connection={"2":{"ip":["default"]},"order":[2]}):
        """_summary_

        Args:
            name (_type_): _description_
            server_ip_address (_type_): _description_
            id (int, optional): _description_. Defaults to 0.
            enable (bool, optional): _description_. Defaults to True.
            protocol (tuple, optional): _description_. Defaults to ("TCP", 554, None).
            allow_pepvpn (bool, optional): _description_. Defaults to False.
            wan_connection (dict, optional): _description_. Defaults to {"2":{"ip":["default"]},"order":[2]}.
        """
        
        func_args = locals()
        self.__check_parameters(func_args)

        self.params = {
            'func': 'config.inbound.service',
            'action': 'add',
            'list': [
                {
                    'id': id,
                    'enable': enable,
                    'name': name,
                    'protocol': {
                        'type': protocol[0],
                        'port': protocol[1],
                        'portMapper': protocol[2]
                    },
                    'allowPepvpnConnection': allow_pepvpn,
                    'wanConnection': wan_connection,
                    'inboundServer': {
                        'action': 'add',
                        'ip': server_ip_address,
                        'name': ''
                    }
                }
            ]
        }

    def __check_parameters(self, parameters):
        if len(parameters['protocol']) != 3:
            raise SyntaxError('Please Provide 3 items for protocol (Protocol, Port, Mapped Port). If mapped port isn\'t applicable then provide None')

class GenericLan(BaseTemplate):

    def __init__(self, lan_mac_custom='on', _ip=None, _mask=24,
                    _gateway=None, lan_static_route_count=0, lan_static_route_order=None,
                    _ntw_type=None, _virtual=None, vnat_o2o_count=0, vnat_m2o_count=0,
                    wins_enable=None, ldns_enable='yes', ldns_use_google='yes', _host=None,
                    _ttl=None, lan_ldns_route_count=0, lan_ldns_route_order=None,
                    _domain=None, _conn=None, ldns_custom_resolver=None, ldns_lan_0_server=None):
        """_summary_

        Args:
            lan_mac_custom (str, optional): _description_. Defaults to 'on'.
            _ip (_type_, optional): _description_. Defaults to None.
            _mask (int, optional): _description_. Defaults to 24.
            _gateway (_type_, optional): _description_. Defaults to None.
            lan_static_route_count (int, optional): _description_. Defaults to 0.
            lan_static_route_order (_type_, optional): _description_. Defaults to None.
            _ntw_type (_type_, optional): _description_. Defaults to None.
            _virtual (_type_, optional): _description_. Defaults to None.
            vnat_o2o_count (int, optional): _description_. Defaults to 0.
            vnat_m2o_count (int, optional): _description_. Defaults to 0.
            wins_enable (_type_, optional): _description_. Defaults to None.
            ldns_enable (str, optional): _description_. Defaults to 'yes'.
            ldns_use_google (str, optional): _description_. Defaults to 'yes'.
            _host (_type_, optional): _description_. Defaults to None.
            _ttl (_type_, optional): _description_. Defaults to None.
            lan_ldns_route_count (int, optional): _description_. Defaults to 0.
            lan_ldns_route_order (_type_, optional): _description_. Defaults to None.
            _domain (_type_, optional): _description_. Defaults to None.
            _conn (_type_, optional): _description_. Defaults to None.
            ldns_custom_resolver (_type_, optional): _description_. Defaults to None.
            ldns_lan_0_server (_type_, optional): _description_. Defaults to None.
        """
                    
        self.params = locals()
        self.params['section'] = 'LAN_generic_modify'
        del self.params['self']

class LanProfile(BaseTemplate):

    def __init__(self, lan_id, lan_dhcp_mode="server", lan_ip='192.168.50.1', lan_mask=24, wan_dropin_self_ip='169.254.0.1',
                    wan_dropin_self_mask=24, lan_name='Default', lan_vlan=None, lan_routing='yes', can_dropin='yes', prev_dropin_conn_id=None, wan_dropin_conn_id=1,
                    wan_dropin_nat_on_vlan='yes', wan_dropin_lan_ip=None, wan_dropin_lan_mask=24, wan_dropin_route=None, wan_dropin_gateway=None,
                    wan_dropin_dns_custom_server1=None, wan_dropin_dns_custom_server2=None, l2_profile=None, l2_pvid=None, l2_override=None, l2_lan_ip=None,
                    l2_lan_mask=24, lan_dhcp_mode_ui='server', lan_dhcp_pool_start='192.168.50.10', lan_dhcp_pool_end='192.168.50.250',
                    lan_dhcp_pool_mask=24, lan_dhcp_lease=28800, lan_dhcp_lease_day_ui=0, lan_dhcp_lease_hour_ui=8, lan_dhcp_lease_minute_ui=0,
                    lan_dhcp_dns_custom_server=None, lan_dhcp_dns_auto='yes', dns_custom_server1=None, dns_custom_server2=None, lan_dhcp_wins_servers=None,
                    lan_dhcp_wins_custom_builtin='no', wins_custom_server1=None, wins_custom_server2=None, dhcp_bootp_server=None, dhcp_bootp_file=None, dhcp_bootp_sn=None,
                    dhcp_reservation_count=0, dhcp_reservation_order=None, lan_dhcp_relay_server=None, dhcp_relay_server1=None, dhcp_relay_server2=None,
                    section='LAN_network_modify'):
        """_summary_

        Args:
            lan_id (_type_): _description_
            lan_dhcp_mode (str, optional): _description_. Defaults to "server".
            lan_ip (str, optional): _description_. Defaults to '192.168.50.1'.
            lan_mask (int, optional): _description_. Defaults to 24.
            wan_dropin_self_ip (str, optional): _description_. Defaults to '169.254.0.1'.
            wan_dropin_self_mask (int, optional): _description_. Defaults to 24.
            lan_name (str, optional): _description_. Defaults to 'Default'.
            lan_vlan (_type_, optional): _description_. Defaults to None.
            lan_routing (str, optional): _description_. Defaults to 'yes'.
            can_dropin (str, optional): _description_. Defaults to 'yes'.
            prev_dropin_conn_id (_type_, optional): _description_. Defaults to None.
            wan_dropin_conn_id (int, optional): _description_. Defaults to 1.
            wan_dropin_nat_on_vlan (str, optional): _description_. Defaults to 'yes'.
            wan_dropin_lan_ip (_type_, optional): _description_. Defaults to None.
            wan_dropin_lan_mask (int, optional): _description_. Defaults to 24.
            wan_dropin_route (_type_, optional): _description_. Defaults to None.
            wan_dropin_gateway (_type_, optional): _description_. Defaults to None.
            wan_dropin_dns_custom_server1 (_type_, optional): _description_. Defaults to None.
            wan_dropin_dns_custom_server2 (_type_, optional): _description_. Defaults to None.
            l2_profile (_type_, optional): _description_. Defaults to None.
            l2_pvid (_type_, optional): _description_. Defaults to None.
            l2_override (_type_, optional): _description_. Defaults to None.
            l2_lan_ip (_type_, optional): _description_. Defaults to None.
            l2_lan_mask (int, optional): _description_. Defaults to 24.
            lan_dhcp_mode_ui (str, optional): _description_. Defaults to 'server'.
            lan_dhcp_pool_start (str, optional): _description_. Defaults to '192.168.50.10'.
            lan_dhcp_pool_end (str, optional): _description_. Defaults to '192.168.50.250'.
            lan_dhcp_pool_mask (int, optional): _description_. Defaults to 24.
            lan_dhcp_lease (int, optional): _description_. Defaults to 28800.
            lan_dhcp_lease_day_ui (int, optional): _description_. Defaults to 0.
            lan_dhcp_lease_hour_ui (int, optional): _description_. Defaults to 8.
            lan_dhcp_lease_minute_ui (int, optional): _description_. Defaults to 0.
            lan_dhcp_dns_custom_server (_type_, optional): _description_. Defaults to None.
            lan_dhcp_dns_auto (str, optional): _description_. Defaults to 'yes'.
            dns_custom_server1 (_type_, optional): _description_. Defaults to None.
            dns_custom_server2 (_type_, optional): _description_. Defaults to None.
            lan_dhcp_wins_servers (_type_, optional): _description_. Defaults to None.
            lan_dhcp_wins_custom_builtin (str, optional): _description_. Defaults to 'no'.
            wins_custom_server1 (_type_, optional): _description_. Defaults to None.
            wins_custom_server2 (_type_, optional): _description_. Defaults to None.
            dhcp_bootp_server (_type_, optional): _description_. Defaults to None.
            dhcp_bootp_file (_type_, optional): _description_. Defaults to None.
            dhcp_bootp_sn (_type_, optional): _description_. Defaults to None.
            dhcp_reservation_count (int, optional): _description_. Defaults to 0.
            dhcp_reservation_order (_type_, optional): _description_. Defaults to None.
            lan_dhcp_relay_server (_type_, optional): _description_. Defaults to None.
            dhcp_relay_server1 (_type_, optional): _description_. Defaults to None.
            dhcp_relay_server2 (_type_, optional): _description_. Defaults to None.
            section (str, optional): _description_. Defaults to 'LAN_network_modify'.
        """

        self.params = locals()
        del self.params['self']

class CellularSettings(BaseTemplate):

    def __init__(self, instant_active=True, apn=None, id=2, name='Cellular', enable=True,
                    healthcheck={'enable': True, 'method': {'type': 'smartcheck', 'detail': {'host': []}}, 'timeout': 5000, 'interval': 10, 'retry': 3, 'recovery': 3},
                    ddns={'enable': False}, schedule=None, cellular={'preferredSim': None, 'simCardScheme': '1'}, sim1_info=None, sim2_info=None, signal_level=0, priority=1, mtu=1342):
        """_summary_

        Args:
            instant_active (bool, optional): _description_. Defaults to True.
            apn (_type_, optional): _description_. Defaults to None.
            id (int, optional): _description_. Defaults to 2.
            name (str, optional): _description_. Defaults to 'Cellular'.
            enable (bool, optional): _description_. Defaults to True.
            healthcheck (dict, optional): _description_. Defaults to {'enable': True, 'method': {'type': 'smartcheck', 'detail': {'host': []}}, 'timeout': 5000, 'interval': 10, 'retry': 3, 'recovery': 3}.
            ddns (dict, optional): _description_. Defaults to {'enable': False}.
            schedule (_type_, optional): _description_. Defaults to None.
            cellular (dict, optional): _description_. Defaults to {'preferredSim': None, 'simCardScheme': '1'}.
            sim1_info (_type_, optional): _description_. Defaults to None.
            sim2_info (_type_, optional): _description_. Defaults to None.
            signal_level (int, optional): _description_. Defaults to 0.
            priority (int, optional): _description_. Defaults to 1.
            mtu (int, optional): _description_. Defaults to 1342.
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
                    'healthcheck': healthcheck,
                    'ddns': ddns,
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
