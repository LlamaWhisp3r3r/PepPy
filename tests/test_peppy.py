import sys
sys.path.insert(1, '../src')
import peppy, templates
import httpretty
import unittest

class TestPepPy(unittest.TestCase):

    def setUp(self):
        self.pep = peppy.PepPy('admin', 'admin')
    
    def __assert_response(func):
        def magic(self, *args, **kwargs):
            r = func(self, *args, **kwargs)
            self.assertTrue(r)
        return magic

    @__assert_response
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def __send_api_mock(self, func, *args, **kwargs):
        httpretty.register_uri(
            httpretty.POST,
            "https://192.168.50.1/cgi-bin/MANGA/api.cgi",
            body='{"stat": "ok"}'
        )
        return func(*args, **kwargs)
    
    @__assert_response
    @httpretty.activate(verbose=False, allow_net_connect=False)
    def __send_admin_mock(self, func, *args, **kwargs):
        httpretty.register_uri(
            httpretty.POST,
            "https://192.168.50.1/cgi-bin/MANGA/admin.cgi",
            body='<status>\n1\n</status>'
        )
        return func(*args, **kwargs)
    
    @__assert_response
    @httpretty.activate(verbose=False, allow_net_connect=False)
    def __send_firmware_mock(self, func, *args, **kwargs):
        httpretty.register_uri(
            httpretty.POST,
            "https://192.168.50.1/cgi-bin/MANGA/firmware.cgi",
            body='<status>\n1\n</status>'
        )
        return func(*args, **kwargs)
    
    def test_login(self):
        self.__send_api_mock(self.pep.login)
    
    def test_password_change(self):
        self.__send_api_mock(self.pep.change_password, 'Test')
    
    def test_ap_change(self):
        self.__send_api_mock(self.pep.change_ap_password, 'Test')
    
    def test_generic_update(self):
        gl = templates.GenericLan()
        self.__send_admin_mock(self.pep.update_generic_lan, gl)

    def test_port_forwarding(self):
        pf = templates.PortForwarding("Test", "192.168.50.5", protocol=("TCP", 80, None))
        self.__send_api_mock(self.pep.add_port_forwarding_rule, pf)
    
    def test_admin_settings(self):
        ads = templates.AdminSettings("Test")
        self.__send_api_mock(self.pep.update_admin_settings, ads)
    
    def test_time_settings(self):
        ts = templates.TimeSettings("Test")
        self.__send_api_mock(self.pep.update_time_settings, ts)
    
    def test_email_settings(self):
        es = templates.EmailSettings("test.com", None, 2525, username="Test.com",
                        password="Test", sender='Test.com', recipients=['Test.com'])
        self.__send_api_mock(self.pep.update_email_notifications, es)
    
    def test_apply_settings(self):
        self.__send_api_mock(self.pep.apply_changes, wait_time=0)
    
    def test_update_firmware(self):
        self.__send_firmware_mock(self.pep.update_firmware, "Test.txt")

    def test_edit_lan(self):
        lp = templates.LanProfile(0)
        self.__send_admin_mock(self.pep.edit_lan, lp)
        
if __name__ == '__main__':
    unittest.main()