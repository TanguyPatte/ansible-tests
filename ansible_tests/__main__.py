import click
from ansible_tests.yaml_loader import YamlLoader
from ansible_tests.testinfra_launcher import TestinfraLauncher


@click.command("ansible-tests")
@click.option("--playbook", "-p", type=click.Path(exists=True, file_okay=True, resolve_path=True),
              help='Name of the playbook or tests description file', required=True)
@click.option("--inventory", "-i", type=click.Path(exists=True, file_okay=True, resolve_path=True),
              help='Name of the inventory', required=True)
def run(file_name, inventory):
    TestinfraLauncher(YamlLoader()).run_test(file_name, inventory)


if __name__ == '__main__':
    run()
