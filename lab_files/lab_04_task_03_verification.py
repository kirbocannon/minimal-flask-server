import re
import json
import yaml
import requests
from tabulate import tabulate
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable any ssl insecure warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CREDENTIALS = ("admin", "1234QWer")


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


def nxapi_json_show_request(host, cmd):
    """Builds and sends a `show` cli command to an nxapi enabled device.

    Args:
        host (str): IP or hostname of device to send to. Note that DNS
            will need to work if you are using the device hostname
        cmd (str): Show command to send to device.

    Returns:
        resp (dict): response from device

    Example:
        >>> nxapi_json_show_request(host=1.1.1.1, cmd='show lldp neighbors')

    """
    # set http headers to accept content type of json
    headers = {"content-type": "application/json"}
    # set url of switch api
    url = f"http://{host}/ins"

    # specify type and command and output type to json
    payload = {
      "ins_api": {
        "version": "1.2",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": cmd,
        "output_format": "json"
      }
    }

    # send REST request
    resp = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        auth=CREDENTIALS,
        verify=False).json()

    return resp


def convert_short_iface_to_long(interface):
    """Converts short interface name such as `Eth1/1` to full name `ETHERNET1/1`
       with all uppercase characters. This will only work for Nexus ethernet and
       port-channel interfaces.

    Args:
        interface (str): Interface name to convert, such as `Eth1/1` or `ETH2/3`.

    Returns:
        long_iface_name (str): This will be the concatenation of `interface_type` and `slot`
            or it will be the original interface if already in long name format. If `interface_type`
            does not equal supported interface names after conversion , then the original interface
            will be returned.

    Examples:
        >>> print(convert_short_iface_to_long('Eth1/2'))
        'ETHERNET1/2`
        >>> print(convert_short_iface_to_long('PO12'))
        'PORT-CHANNEL12`

    """
    interface = interface.upper()
    interface_type = ''
    slot = ''
    supported_names = ['ETHERNET', 'PORT-CHANNEL']

    if 'ETHERNET' in interface or 'PORT-CHANNEL' in interface:
        long_iface_name = interface

    else:
        if interface.startswith('ETH'):
            interface_type = 'ETHERNET'
            slot = re.split('ETH', interface)[1]
        elif interface.startswith('ET'):
            interface_type = 'ETHERNET'
            slot = re.split('ET', interface)[1]
        elif interface.startswith('PO'):
            interface_type = 'PORT-CHANNEL'
            slot = re.split('PO', interface)[1]

        if interface_type not in supported_names:
            long_iface_name = interface
        else:
            long_iface_name = interface_type + slot

    return long_iface_name


def main():
    verify_file = read_yaml_file("verification.yaml")

    # get host ip address information from configuration file
    # this returns a dictionary which we will use to get the switch's IP
    inventory = verify_file["hosts"]
    intended_connections = verify_file['connections']
    lldp_results = []
    interfaces_results = []
    vpc_results = []

    # hostname = 'N7K-B-Pod6'
    # host = inventory[hostname]['mgmt_ip']

    # normally you'd want to batch these commands together in one call
    # but showing seperate calls here for simplicity
    for hostname, details in inventory.items():

        lldp_neighbors = nxapi_json_show_request(
            host=details['mgmt_ip'],
            cmd='show lldp neighbors',
        )

        interface_status = nxapi_json_show_request(
            host=details['mgmt_ip'],
            cmd='show interface status'
        )

        vpc_status = nxapi_json_show_request(
            host=details['mgmt_ip'],
            cmd='show vpc brief',
        )

        # Compare lldp information and keep track of any discrepancy with intended config
        # This assumes LLDP information is provided in the `verification.yaml` file
        for connection in intended_connections:
            if connection['device'] == hostname:
                rdict = {'hostname': hostname, 'intended_connection': connection, 'status': '', 'errors': []}
                if connection.get('neighbor') and connection.get('neighbor_interface'):
                    intended_neighbor_hostname = connection['neighbor'].upper()
                    intended_local_interface = connection['interface'].upper()
                    intended_neighbor_interface = connection['neighbor_interface'].upper()

                    # get live lldp information
                    for entry in lldp_neighbors['ins_api']['outputs']['output']['body']['TABLE_nbor']['ROW_nbor']:
                        current_neighbor_hostname = entry['chassis_id'].upper()
                        current_local_interface = entry['l_port_id'].upper()
                        current_neighbor_interface = entry['port_id'].upper()

                        # use local interface as key
                        if intended_local_interface == current_local_interface:
                            if not intended_neighbor_hostname == current_neighbor_hostname:
                                rdict['errors'].append(f"Intended neighbor hostname is {intended_neighbor_hostname}"
                                                       f" but current neighbor hostname is {current_neighbor_hostname}")
                                rdict['status'] = 'ERROR'
                            if not intended_neighbor_interface == current_neighbor_interface:
                                rdict['errors'].append(f"Intended neighbor interface is {intended_neighbor_interface}"
                                                       f" but current neighbor interface is {current_neighbor_interface}")
                                rdict['status'] = 'ERROR'

                            if rdict['status'] != 'ERROR':
                                rdict['status'] = 'OK'
                            break

                    if not rdict['status']:
                        rdict['errors'].append(f"{intended_local_interface} not found")
                        rdict['status'] = 'ERROR'

                lldp_results.append(rdict)

        # now we check for vlan interface status in the `verification.yaml` file
        intended_interfaces = verify_file['interfaces'].get(hostname)
        if intended_interfaces:
            current_interface_status = interface_status['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']

            for intended_interface_name, details in intended_interfaces.items():
                rdict = {'hostname': hostname,
                         'intended_interface_status': {intended_interface_name: details},
                         'status': '',
                         'errors': []}
                intended_interface_name = convert_short_iface_to_long(intended_interface_name)
                rdict['interface'] = intended_interface_name
                intended_interface_state = details['state'].upper()
                for current_interface in current_interface_status:
                    current_interface_name = convert_short_iface_to_long(current_interface['interface'])
                    current_interface_state = current_interface['state'].upper()
                    if intended_interface_name == current_interface_name:
                        if intended_interface_state == current_interface_state:
                            rdict['status'] = 'OK'
                        else:
                            rdict['errors'].append(f"Intended interface state for {intended_interface_name}"
                                                   f" is {intended_interface_state} but current interface state"
                                                   f" is {current_interface_state}")
                            rdict['status'] = 'ERROR'
                        break

                if not rdict['status']:
                    rdict['errors'].append(f"{intended_interface_name} not found")
                    rdict['status'] = 'ERROR'

                interfaces_results.append(rdict)

        # now we will check for any switch VPC issues between two peer devices
        intended_vpc = verify_file['vpc'][hostname]
        vdict = {
            'hostname': hostname,
            'intended_vpc_status': intended_vpc,
            'current_vpc_status': {},
            'status': '',
            'vlans_not_found': [],
            'errors': []
        }

        current_vpc_status = vpc_status['ins_api']['outputs']['output']['body']

        # if VPC is enabled, do the vpc status check, otherwise skip this check
        if current_vpc_status.get('TABLE_peerlink'):

            intended_domain_id = str(intended_vpc['system']['domain_id'])
            intended_role = intended_vpc['system']['role'].upper()
            intended_peer_status = intended_vpc['system']['peer_status'].upper()
            intended_consistency_type_1 = intended_vpc['system']['consistency']['type1'].upper()
            intended_consistency_type_2 = intended_vpc['system']['consistency']['type2'].upper()

            current_domain_id = current_vpc_status['vpc-domain-id']
            current_role = current_vpc_status['vpc-role'].upper()
            current_peer_status = current_vpc_status['vpc-peer-status'].upper()
            current_consistency_type_1 = current_vpc_status['vpc-peer-consistency-status'].upper()
            current_consistency_type_2 = current_vpc_status['vpc-type-2-consistency-status'].upper()

            if intended_domain_id != current_domain_id:
                vdict['errors'].append(f"Intended vpc domain id is {intended_domain_id}"
                                       f" but the current vpc domain id is {current_domain_id}")
                vdict['status'] = 'ERROR'
            if intended_role != current_role:
                vdict['errors'].append(f"Intended vpc role is {intended_role}"
                                       f" but current vpc role is {current_role}")
                vdict['status'] = 'ERROR'
            if intended_peer_status != current_peer_status:
                vdict['errors'].append(f"Intended vpc peer status {intended_peer_status}"
                                       f" but current vpc peer status is {current_peer_status}")
                vdict['status'] = 'ERROR'
            if intended_consistency_type_1 != current_consistency_type_1:
                vdict['errors'].append(f"Intended vpc type 1 consistency check is {intended_consistency_type_1}"
                                       f" but current vpc type 2 consistency check is {current_consistency_type_2}")
                vdict['status'] = 'ERROR'
            if intended_consistency_type_2 != current_consistency_type_2:
                vdict['errors'].append(f"Intended vpc type 2 consistency check is {intended_consistency_type_2}"
                                       f" but current vpc type 2 consistency check is {current_consistency_type_2}")
                vdict['status'] = 'ERROR'

            intended_vpc_peer_link_interface_name = intended_vpc['peer_link']['interface']
            intended_vpc_peer_link_interface_status = intended_vpc['peer_link']['status'].upper()
            intended_vpc_peer_link_interface_name = convert_short_iface_to_long(intended_vpc_peer_link_interface_name)
            intended_active_vlans = intended_vpc['peer_link']['active_vlans']
            #if current_vpc_status.get('TABLE_peerlink'):
            current_vpc_peer_link_interface_name = convert_short_iface_to_long(
                current_vpc_status['TABLE_peerlink']['ROW_peerlink']['peerlink-ifindex'])
            current_active_vlans = current_vpc_status['TABLE_peerlink']['ROW_peerlink']['peer-up-vlan-bitset'].split(',')

            if intended_vpc_peer_link_interface_name != current_vpc_peer_link_interface_name and \
                    intended_vpc_peer_link_interface_status == 'UP':
                vdict['errors'].append(f"Intended vpc peer link interface is {intended_vpc_peer_link_interface_name}"
                                       f" but current vpc peer link interface is {current_vpc_peer_link_interface_name}")
                vdict['status'] = 'ERROR'

            if len(intended_active_vlans) != len(current_active_vlans):
                vdict['errors'].append(f"Intended active vlans are {intended_active_vlans}"
                                       f" but current active vlans are {current_active_vlans}")
                vdict['status'] = 'ERROR'

            for intended_active_vlan in intended_active_vlans:
                intended_active_vlan = str(intended_active_vlan)
                if intended_active_vlan not in current_active_vlans:
                    vdict['vlans_not_found'].append(intended_active_vlan)
                    vdict['status'] = 'ERROR'

            if vdict['status'] != 'ERROR':
                vdict['status'] = 'OK'

            vpc_results.append(vdict)

    # display lldp esults in a table
    ldict = {
        'hostname': [],
        'status': []
    }

    lldp_error_details = []

    for result in lldp_results:
        ldict['hostname'].append(result['hostname'])
        ldict['status'].append(result['status'])
        lldp_error_details.append({'hostname': result['hostname'], 'errors': result['errors']})

    print('------------------LLDP STATUS------------------')
    tabulated_table = tabulate(ldict,
                               headers="keys", tablefmt="fancy_grid")

    print(tabulated_table, '\n')
    for errors in lldp_error_details:
        for error in errors['errors']:
            print(f"--> {errors['hostname']}: {error}")
    print('\n')

    # display interface results in a table
    print('------------------INTERFACE STATUS------------------')
    idict = {
        'hostname': [],
        'interface': [],
        'status': []
    }

    interfaces_error_details = []

    for result in interfaces_results:
        idict['hostname'].append(result['hostname'])
        idict['interface'].append(result['interface'])
        idict['status'].append(result['status'])
        interfaces_error_details.append({'hostname': result['hostname'], 'errors': result['errors']})

    tabulated_table = tabulate(idict,
                               headers="keys", tablefmt="fancy_grid")

    print(tabulated_table, '\n')

    for errors in interfaces_results:
        for error in errors['errors']:
            print(f"--> {errors['hostname']}: {error}")
    print('\n')

    # display vpc results in a table
    tdict = {
        'hostname': [],
        'status': []
    }

    vpc_error_details = []

    for result in vpc_results:
        tdict['hostname'].append(result['hostname'])
        tdict['status'].append(result['status'])
        vpc_error_details.append({'hostname': result['hostname'], 'errors': result['errors']})

    print('------------------VPC STATUS------------------')
    tabulated_table = tabulate(tdict,
                               headers="keys", tablefmt="fancy_grid")

    print(tabulated_table, '\n')

    for errors in vpc_error_details:
        for error in errors['errors']:
            print(f"--> {errors['hostname']}: {error}")
    print('\n')


if __name__ == "__main__":
    main()
