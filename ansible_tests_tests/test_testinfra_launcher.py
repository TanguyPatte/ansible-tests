from unittest import TestCase
from unittest.mock import Mock, patch, call
from ansible_tests.testinfra_launcher import TestinfraLauncher
from ansible_tests.yaml_loader import YamlLoader
import os
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_FILE_PATH = os.path.join(CURRENT_PATH, 'test.yml')
COMMAND_PATH = '/home/bob/ansible'

class TestinfraLauncherTest(TestCase):

    def test_run_subprocess_with_dev_inventory(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/dev.ini --hosts=ansible://all /home/bob/ansible/roles/base/tests'.split(' ')
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(YamlLoader())
                inventory = COMMAND_PATH + "/inventories/dev.ini"
                testinfra_launcher.run_test(TEST_FILE_PATH, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_prod_inventory(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://all /home/bob/ansible/roles/base/tests'.split(' ')
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(YamlLoader())
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(TEST_FILE_PATH, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_2_roles(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests /home/bob/ansible/roles/mysql/tests'.split(' ')

        yaml_content = [{
            'hosts': ['bdd'],
            'roles': ['base', 'mysql']
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_2_hosts(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd,web /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': ['bdd', 'web'],
            'roles': ['base']
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_2_tests(self):
        expected_command1 = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd,web /home/bob/ansible/roles/base/tests'.split(' ')
        expected_command2 = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://rp,bastion /home/bob/ansible/roles/secu/tests /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': ['bdd', 'web'],
            'roles': ['base']
        }, {
            'hosts': ['rp', 'bastion'],
            'roles': ['secu', 'base']
        }
        ]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_has_calls([call(expected_command1), call(expected_command2)])

    def test_run_subprocess_with_1_host_not_in_list(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd',
            'roles': ['base']
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_1_role_not_in_list(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd',
            'roles': 'base'
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_1_role_in_dict(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd',
            'roles': [{'role': 'base'}]
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_2_hosts_separated_by_colon(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd,web /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd:web',
            'roles': [{'role': 'base'}]
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.return_value = True
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)
#os.path.exists("/etc")

    def test_run_subprocess_with_2_role_in_dict_when_one_directory_does_not_exist(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd',
            'roles': [{'role': 'base'}, {'role': 'nginx'}]
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.side_effect = [True, False]
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)

    def test_run_subprocess_with_2_role_in_arry_when_one_directory_does_not_exist(self):
        expected_command = 'pytest --connection=ansible --ansible-inventory=/home/bob/ansible/inventories/prod.ini --hosts=ansible://bdd /home/bob/ansible/roles/base/tests'.split(' ')

        yaml_content = [{
            'hosts': 'bdd',
            'roles': ['base', 'nginx']
        }]
        yaml_loader_mock = Mock()
        yaml_loader_mock.load.return_value = yaml_content
        with patch('os.path.exists') as patch_exists:
            patch_exists.side_effect = [True, False]
            with patch('subprocess.run') as patch_subprocess_run:
                testinfra_launcher = TestinfraLauncher(yaml_loader_mock)
                file_name = "test.yml"
                inventory = "/home/bob/ansible/inventories/prod.ini"
                testinfra_launcher.run_test(file_name, inventory, COMMAND_PATH)
                patch_subprocess_run.assert_called_once_with(expected_command)
