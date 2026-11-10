"""Small offline regression checks; real provider edge/TLS still needs testing."""
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
import main


class SubscriptionRegressionTests(unittest.TestCase):
    def test_status_preserves_real_connection_not_a_synthetic_ws_route(self):
        user = {"username": "test", "config_uuid": "not-used", "traffic_limit_bytes": 0}
        configs = [
            "vless://11111111-1111-4111-8111-111111111111@worker.example:443?security=tls&type=ws&host=worker.example&path=%2Fws%2F11111111-1111-4111-8111-111111111111#Worker",
            "vless://22222222-2222-4222-8222-222222222222@node.example:8443?security=reality&type=xhttp&path=%2F&pbk=key#Reality",
            "vless://33333333-3333-4333-8333-333333333333@node.example:443?security=tls&type=ws&path=%2Fcustom%2Fpath#Node",
        ]
        for config in configs:
            with self.subTest(config=config):
                status = main.generate_status_config(user, [config])
                self.assertEqual(status.split('#', 1)[0], config.split('#', 1)[0])
        self.assertEqual(main.generate_status_config(user, []), '')
        self.assertEqual(main.generate_status_config(user, ['vmess://encoded']), '')

    def test_provider_launcher_port_and_railway_default(self):
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual(main._env_port(), 8080)
        with patch.dict('os.environ', {'RAHGOZAR_LISTEN_PORT': '18081'}, clear=True):
            self.assertEqual(main._env_port(), 18081)
        with patch.dict('os.environ', {'RAHGOZAR_LISTEN_PORT': 'bad'}, clear=True):
            self.assertEqual(main._env_port(), 8080)

    def test_existing_node_key_is_not_renamed(self):
        self.assertEqual(main._normalize_node_key('spdr_existing-secret'), 'spdr_existing-secret')
        self.assertEqual(main._normalize_node_key('rgz_existing-secret'), 'rgz_existing-secret')

    def test_upstream_protocols_have_managed_relay_config(self):
        for kind, protocol in [('vmess', 'vmess://'), ('trojan', 'trojan://'), ('shadowsocks', 'ss://')]:
            with self.subTest(kind=kind):
                inbound = main._relays._fixed_inbound(kind, 'panel.example')
                self.assertTrue(main._is_panel_relay_inbound('relay_' + kind, inbound))
                config = main._relays.client_config(kind, '11111111-1111-4111-8111-111111111111', 'panel.example', '443', 'panel.example', 'test')
                self.assertTrue(config.startswith(protocol))

    def test_standalone_stream_one_uses_supported_stream_up(self):
        with patch.object(main, '_safe_host', return_value='panel.example'):
            link = main.generate_vless_link('11111111-1111-4111-8111-111111111111', 'panel.example', protocol='xhttp-stream-one')
        query = parse_qs(urlsplit(link).query)
        self.assertEqual(query['mode'], ['stream-up'])
        self.assertTrue(query['path'][0].startswith('/xhttp-siz10/stream-up/'))

if __name__ == '__main__':
    unittest.main()
