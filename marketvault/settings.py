import yaml


with open("settings.yaml", "r") as s_file:
    settings = yaml.safe_load(s_file)
