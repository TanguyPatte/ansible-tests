import subprocess
import re
import os

class TestinfraLauncher:

    def __init__(self, yaml_loader):
        self.yaml_loader = yaml_loader

    def run_test(self, file_name, inventory, current_path):
        tests = self.yaml_loader.load(file_name)
        for test in tests:
            command = build_command(test, inventory, current_path)
            subprocess.run(command.split(' '))


def build_tests_path(roles, current_path):
    result = ''
    if isinstance(roles, str):
        return ' {}/roles/{}/tests'.format(current_path, roles)
    for role in roles:
        if isinstance(role, dict):
            if os.path.exists('{}/roles/{}/tests'.format(current_path, role['role'])):
                result += ' {}/roles/{}/tests'.format(current_path, role['role'])
        else:
            if os.path.exists('{}/roles/{}/tests'.format(current_path, role)):
                result += ' {}/roles/{}/tests'.format(current_path, role)
    return result


def build_command(test_content, inventory, current_path):
    hosts = build_hosts_list(test_content['hosts'])
    roles = test_content['roles']
    tests_path = build_tests_path(roles, current_path)
    return 'pytest --connection=ansible --ansible-inventory=' + inventory + ' --hosts=ansible://' + hosts + tests_path


def build_hosts_list(hosts):
    if isinstance(hosts, list):
        return ','.join(hosts)
    return re.sub(':', ',', hosts)
