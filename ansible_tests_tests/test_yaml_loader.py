from unittest import TestCase
import os
from ansible_tests.yaml_loader import YamlLoader

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))


class YamlLoaderTest(TestCase):

    def test_load_yaml_file(self):
        expected_result = [
            {
                'hosts': ['all'],
                'roles': ['base']
            }
        ]
        yaml_loader = YamlLoader()
        self.assertEqual(expected_result, yaml_loader.load(os.path.join(CURRENT_PATH, 'test.yml')))
