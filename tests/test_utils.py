import requests

from unittest import mock, TestCase, skip

from protonvpn_cli.utils import (
    call_api,
    get_ip_info,
    cidr_to_netmask,
    get_country_name,
)


class TestUtils(TestCase):

    @mock.patch('protonvpn_cli.utils.requests.get')
    def test_call_api(self, get):
        api_url = 'https://api.protonvpn.ch{}'
        test_headers = {
            'x-pm-appversion': 'Other',
            'x-pm-apiversion': '3',
            'Accept': 'application/vnd.protonmail.v1+json'
        }

        call_api('/test_endpoint')
        get.assert_called_once_with(
            api_url.format('/test_endpoint'),
            headers=test_headers
        )
        get.reset_mock()

        call_api('/test_endpoint2', json_format=False)
        get.assert_called_once_with(
            api_url.format('/test_endpoint2'),
            headers=test_headers
        )
        get.reset_mock()

        call_api('/test_endpoint3', handle_errors=False)
        get.assert_called_once_with(
            api_url.format('/test_endpoint3'),
            headers=test_headers
        )
        get.reset_mock()

    @mock.patch('protonvpn_cli.utils.logger.debug')
    @mock.patch('protonvpn_cli.utils.requests.get')
    def test_call_api_excpt(self, get, debug):
        get.side_effect = requests.exceptions.ConnectionError()
        with self.assertRaises(SystemExit):
            call_api('/test_endpoint')
        get.assert_called_once()
        debug.assert_called_with('Error connecting to ProtonVPN API')
        get.reset_mock(side_effect=True)

    @mock.patch('protonvpn_cli.utils.call_api')
    def test_get_ip_info(self, call_api):
        call_api.return_value = {'IP': 'testIP', 'ISP': 'testISP'}
        ip, isp = get_ip_info()
        self.assertEqual(ip, 'testIP')
        self.assertEqual(isp, 'testISP')

    def test_get_country_name(self):
        self.assertEqual(get_country_name('US'), 'United States')

        # country code does not exist
        self.assertEqual(get_country_name('USSR'), 'USSR')

    def test_cidr_to_netmask(self):
        self.assertEqual(cidr_to_netmask(24), '255.255.255.0')
        self.assertEqual(cidr_to_netmask(32), '255.255.255.255')
        self.assertEqual(cidr_to_netmask(0), '0.0.0.0')
