import click
from ansible_tests.yaml_loader import YamlLoader
from ansible_tests.testinfra_launcher import TestinfraLauncher
import os


@click.command("ansible-tests")
@click.option("--playbook", "-p", type=click.Path(exists=True, file_okay=True, resolve_path=True),
              help='Name of the playbook or tests description file', required=True)
@click.option("--inventory", "-i", type=click.Path(exists=True, file_okay=True, resolve_path=True),
              help='Name of the inventory', required=True)
def run(playbook, inventory):
    current_path = os.getcwd()
    TestinfraLauncher(YamlLoader()).run_test(playbook, inventory, current_path)


if __name__ == '__main__':
    run()
