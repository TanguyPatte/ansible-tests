import yaml


class YamlLoader:

    def load(self, file_name):
        with open(file_name, 'r') as stream:
            result = yaml.load(stream)
        return result
