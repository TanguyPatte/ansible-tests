import subprocess
import re


class TestinfraLauncher:

    def __init__(self, yaml_loader):
        self.yaml_loader = yaml_loader

    def run_test(self, file_name, inventory):
        tests = self.yaml_loader.load(file_name)
        for test in tests:
            command = build_command(test, inventory)
            subprocess.run(command)


def build_tests_path(roles):
    result = ''
    if isinstance(roles, str):
        return ' roles/' + roles + '/tests'
    for role in roles:
        if isinstance(role, dict):
            result += ' roles/' + role['role'] + '/tests'
        else:
            result += ' roles/' + role + '/tests'
    return result


def build_command(test_content, inventory):
    hosts = build_hosts_list(test_content['hosts'])
    roles = test_content['roles']
    tests_path = build_tests_path(roles)
    return 'pytest --connection=ansible --ansible-inventory=' + inventory + ' --hosts=ansible://' + hosts + tests_path


def build_hosts_list(hosts):
    if isinstance(hosts, list):
        return ','.join(hosts)
    return re.sub(':', ',', hosts)
