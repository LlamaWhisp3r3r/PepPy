import requests
import urllib3
import time

# Disable a printed warning for the requests module
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PepPy:

    def __init__(self, username, password, ip_address="192.168.50.1", port=443, http_type="https", debug=False):
        """ Creates a python module that integrates with the Peplink API.

        Args:
            username (str): Username to log into Peplink router
            password (str): Password to log into Peplink router
            ip_address (str, optional): IP Address of Peplink router. Defaults to "192.168.50.1".
            port (int, optional): Usually the HTTPS or HTTP port to communicate with Peplink. Defaults to 443.
            http_type (str, optional): The HTTP protocol to use. Can either be HTTPS or HTTP. Defaults to "https".
            debug (bool, optional): If True, it will display debuging messages. Defaults to False.
        """

        self.username = username
        self.password = password
        self.__ip = ip_address
        self.__port = port
        self.__http_type = http_type
        self.__DEBUG = debug
        self.__URL = None
        self.__OVERALL_ENDPOINT = "api.cgi"
        self.__ADMIN_ENDPOINT = "admin.cgi"
        self.__FIRMWARE_ENDPOINT = "firmware.cgi"
        self.cookies  = None
        self.__update_url()
    
    @property
    def ip(self):
        return self.__ip
    
    @ip.setter
    def ip(self, new_ip):
        self.__ip = new_ip
        self.__update_url()
    
    def __update_url(self):
        self.__URL = self.__http_type + "://" + self.__ip + ":" + str(self.__port) + "/cgi-bin/MANGA/"
    
    def __debug(self, message):
        if self.__DEBUG:
            print(message)

    def __check_peplink_response(func):
        def magic(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            result = self.__check_if_good_response(response)
            return result
        return magic
    
    def __check_if_good_response(self, response):
        if 'ok' in response.text or 'Success' in response.text:
            return True
        elif '1' in response.text.split('\n'):
            return True
        else:
            return False

    def __send_correct_request(self, endpoint, clean=True, get=False, **kwargs):
        url = self.__URL + endpoint

        self.__debug(f"Sending a request to: {url}")

        # Need to clean the parameters = None or else the peplink API will throw an error
        if clean:
            self.__clean(kwargs)

        if get:
            response = requests.get(url, verify=False, cookies=self.cookies, **kwargs)
        else:
            response = requests.post(url, verify=False, cookies=self.cookies, **kwargs)

        self.__check_for_new_cookies_in_reponse(response)
        return response

    def __clean(self, params):
        if type(params) == list:
            return [self.__clean(e) for e in params]
        elif type(params) == dict:
            for k, v in list(params.items()):
                if v is None:
                    del params[k]
                else:
                    params[k] = self.__clean(v)
        return params
    
    def __check_for_new_cookies_in_reponse(self, response):
        try:
            response.cookies['bauth'] # bauth is where peplink stores the cookie as
            new_cookies = response.cookies
            self.__update_cookies(new_cookies)
        except KeyError:
            pass 
    
    def __update_cookies(self, new_cookies):
        self.cookies  = new_cookies
    
    @__check_peplink_response
    def apply_changes(self, wait_time=15):
        """ Apply changes made to the peplink. This usually takes a couple seconds to take effect

        Args:
            wait_time (int, optional): Time to wait after applying changes. Defaults to 15.

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Applying Changes")

        params = {'func': 'cmd.config.apply'}

        result = self.__send_correct_request(self.__OVERALL_ENDPOINT, data=params)
        time.sleep(wait_time) # Need to wait some time for the settings to take effect
        self.__update_url()
        return result

    @__check_peplink_response
    def login(self):
        """ Log into peplink router

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Logging in")

        params = {
            'username': self.username,
            'password': self.password,
            'func': 'login'
        }

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params)

    @__check_peplink_response
    def change_password(self, new_password):
        """ Change password for current logged on user

        Args:
            new_password (str): New password to replace the old password

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Changing Password")
        
        params = {
            'password': self.password,
            'newPassword': new_password,
            'func': 'cmd.password'
        }

        result = self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params)
        self.password = new_password
        return result
    
    @__check_peplink_response
    def edit_lan(self, lan_profile): 
        """ Edit lan configuration for peplink router under: Network > Network Settings > LAN

        Args:
            lan_profile (templates.LanProfile): LanProfile data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Editting Lan")

        params = lan_profile.params

        result = self.__send_correct_request(self.__ADMIN_ENDPOINT, data=params)
        self.ip = params['lan_ip']
        return result
    
    @__check_peplink_response
    def update_generic_lan(self, generic_lan):
        """ Update Generic Lan information under: Network > Network Settings

        Args:
            generic_lan (templates.GenericLan): Generic Lan data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Generic Lan")

        params = generic_lan.params

        return self.__send_correct_request(self.__ADMIN_ENDPOINT, data=params)

    @__check_peplink_response
    def add_port_forwarding_rule(self, port_forwarding):
        """ Add port forwarding rule to peplink router under: Advanced > Port Forwarding

        Args:
            port_forwarding (tempaltes.PortForwarding): Port forwarding data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """
        
        self.__debug("Adding Port Forwarding Policy")
        params = port_forwarding.params
        
        return self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params)
    
    @__check_peplink_response
    def update_admin_settings(self, admin_settings):
        """ Update the Admin Settings under: System > Admin Security

        Args:
            admin_settings (templates.AdminSettings): Admin Settings data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Admin Settings")
        params = admin_settings.params

        result = self.__send_correct_request(self.__OVERALL_ENDPOINT, data=params)
        self.__port = params['accessProtocol_https_port']
        return result
    
    @__check_peplink_response
    def update_time_settings(self, time_settings):
        """ Update Time Settings under: System > Time

        Args:
            time_settings (tempaltes.TimeSettings): Time Settings data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Time Settings")
        params = time_settings.params

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params)
    
    @__check_peplink_response
    def change_ap_password(self, new_password):
        """ Change the main wifi password

        Args:
            new_password (str): The new password to change the old one to

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Changing AP Password")
        params = {
            'newPassword': new_password,
            'func': 'cmd.ap.password'
        }

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params)
    
    @__check_peplink_response
    def update_email_notifications(self, email_settings):
        """ Update Email Notifications under: System > Email Notification

        Args:
            email_settings (templates.EmailSettings): Email Settings data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Email Settings")
        params = email_settings.params

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, json=params, clean=False)

    @__check_peplink_response
    def update_firmware(self, firmware_file_location):
        """ Update firmware to specificed firmware file

        Args:
            firmware_file_location (str): File path to firmware file. Must be accessable by the running machine

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Firmware")
        params = {'upfile': open(firmware_file_location, 'rb')}

        return self.__send_correct_request(self.__FIRMWARE_ENDPOINT, files=params)
    
    @__check_peplink_response
    def update_cellular(self, cellular_settings):
        """ Update Cellular Settings under: Dashboard > Wan Connection Status > Cellular

        Args:
            cellular_settings (templates.CellularSettings): Cellular Settings data holder

        Returns:
            bool: True if the Peplink accepted the API Call
        """

        self.__debug("Updating Cellular")
        params = cellular_settings.params

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, clean=False, json=params)

    def get_ap_profile(self):
        """ Get Wifi Profile settings

        Returns:
            dict: All the data that was given from the request
        """

        params = {'func': 'config.ap.profile'}

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, params=params, get=True).json()['response']
    
    def get_device_info(self):
        """ Get deivce information

        Returns:
            dict: All the data that was given from the request
        """

        params = {'func': 'status.system.info'}

        return self.__send_correct_request(self.__OVERALL_ENDPOINT, params=params, get=True).json()['response']
    
    def get_mac_address(self):

        results = self.get_device_info()
        return results['macInfo'][0]['mac']
    
    def get_model(self):

        results = self.get_device_info()
        return results['device']['model']
    
    def get_serial_number(self):

        results = self.get_device_info()
        return results['device']['serialNumber']
    
    def get_firmware_version(self):

        results = self.get_device_info()
        return results['device']['firmwareVersion']
    
    def get_uptime(self):

        results = self.get_device_info()
        return results['uptime']['string']
    
    def get_device_name(self):

        results = self.get_device_info()
        return results['device']['name']

    def get_cpu_load(self):

        results = self.get_device_info()
        return results['cpuLoad']['string']
    
    def get_wan_connection_info(self):

        params = {'func': 'status.wan.connection'}
        return self.__send_correct_request(self.__OVERALL_ENDPOINT, params=params, get=True).json()['response']
    
    def get_imei(self):

        results = self.get_wan_connection_info()
        return results['2']['cellular']['imei']