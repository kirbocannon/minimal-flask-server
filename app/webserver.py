import json
import yaml
import app.config as config
from flask import Flask, render_template, \
    jsonify
from app.mock_results import lldp_results, \
    vpc_results, interfaces_results


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
    inventory = verify_file.get('hosts', {})

    for hostname, details in inventory.items():
        details['status'] = '-'

    return inventory


# @app.route('/api/inventory', methods=['GET'])
# def get_inventory():
#     verify_file = read_yaml_file(VERIFICATION_FILEPATH)
#     inventory = []
#     for hostname, details in verify_file.get('hosts', {}).items():
#         inventory.append(hostname)
#
#     return jsonify(inventory)


@app.route('/api/check-health', methods=['GET'])
def check_health():
    import time
    time.sleep(5)
    print('running...')
    hostnames = []
    data = {
        'lldp_results': lldp_results,
        'interfaces_results': interfaces_results,
        'vpc_results': vpc_results
    }
    status_results = {}

    # get list of inventory hostnames
    for hostname, details in load_inventory().items():
        if hostname not in hostnames:
            hostnames.append(hostname)

    for ohostname in hostnames:
        status_results[ohostname] = {'status': '', 'errors': []}
        hostname = ohostname.upper()
        for entry in data['lldp_results']:
            if hostname == entry['hostname'].upper():
                if entry['status'] == 'ERROR':
                    status_results[ohostname]['status'] = 'ERROR'
                    status_results[ohostname]['errors'].extend(entry['errors'])

        for entry in data['interfaces_results']:
            if hostname == entry['hostname'].upper():
                if entry['status'] == 'ERROR':
                    status_results[ohostname]['status'] = 'ERROR'
                    status_results[ohostname]['errors'].extend(entry['errors'])

        for entry in data['vpc_results']:
            if hostname == entry['hostname'].upper():
                if entry['status'] == 'ERROR':
                    status_results[ohostname]['status'] = 'ERROR'
                    status_results[ohostname]['errors'].extend(entry['errors'])

        if status_results[ohostname]['status'] != 'ERROR':
            status_results[ohostname]['status'] = 'OK'

    #print(json.dumps(data, indent=4))
    # print(json.dumps(status_results, indent=4))

    #return jsonify(data)
    return jsonify(status_results)


if __name__ == '__main__':

    mode = 'development'

    if mode == 'development':
        app.config.from_object(config.Development)
    elif mode == 'production':
        app.config.from_object(config.Production)
    app.run()
