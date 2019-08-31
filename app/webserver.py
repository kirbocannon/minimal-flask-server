import os
import yaml
import app.config as config
from flask import Flask, render_template


app = Flask(__name__)

VERIFICATION_FILEPATH = '../lab_files/verification.yaml'

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    inventory = load_inventory()

    return render_template('index.html', inventory=inventory)


def read_yaml_file(filepath):
    """Reads a yaml file and returns a dictionary of elements
       within that yaml file

    Args:
        filepath (str): relative or absolute filepath of yaml file to read

    Returns:
        data (dict): Dictionary of elements within the yaml file

    """

    with open(filepath, "r") as stream:
        data = yaml.safe_load(stream)

    return data


def load_inventory():
    verify_file = read_yaml_file(VERIFICATION_FILEPATH)
    inventory = verify_file.get('hosts', [])

    for hostname, details in inventory.items():
        details['vpc'] = '-'
        details['connections'] = '-'

    return inventory


if __name__ == '__main__':

    mode = 'development'

    if mode == 'development':
        app.config.from_object(config.Development)
        app.run()
    elif mode == 'production':
        app.config.from_object(config.Production)
        app.run()
