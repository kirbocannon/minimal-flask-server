import os
import re
import json
import yaml
import requests
from jinja2 import Environment, FileSystemLoader
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable any ssl insecure warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CREDENTIALS = ("USERNAME", "PASSWORD")


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


def nxapi_send_config_cmds(host, cmds):
    """Builds a request and sends a list of configuration cli commands to an nxapi enabled device.

    Args:
        host (str): IP or hostname of device to send to. Note that DNS
            will need to work if you are using the device hostname
        cmds (:obj: `list` of :obj: `str`): Configuration commands to send to device.

    Returns:
        resp (dict): response from device

    Example:
        >>> nxapi_send_config_cmds(host=1.1.1.1, cmds=['interface vlan 100; description TEST'])

    """
    # set http headers to accept content type of json
    headers = {"content-type": "application/json"}
    # set url of switch api
    url = f"http://{host}/ins"

    # convert command list into one string with each command separated by ` ;`
    cmds = " ;".join(cmds)

    # specify type and command and output type to json
    payload = {
        "ins_api": {
            "version": "1.2",
            "type": "cli_conf",
            "chunk": "0",
            "sid": "1",
            "input": cmds,
            "output_format": "json",
        }
    }

    print(payload)

    # send REST request
    resp = requests.post(
        url, headers=headers, data=json.dumps(payload), auth=CREDENTIALS, verify=False
    ).json()

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
    interface_type = ""
    slot = ""
    supported_names = ["ETHERNET", "PORT-CHANNEL"]

    if "ETHERNET" in interface or "PORT-CHANNEL" in interface:
        long_iface_name = interface

    else:
        if interface.startswith("ETH"):
            interface_type = "ETHERNET"
            slot = re.split("ETH", interface)[1]
        elif interface.startswith("ET"):
            interface_type = "ETHERNET"
            slot = re.split("ET", interface)[1]
        elif interface.startswith("PO"):
            interface_type = "PORT-CHANNEL"
            slot = re.split("PO", interface)[1]

        if interface_type not in supported_names:
            long_iface_name = interface
        else:
            long_iface_name = interface_type + slot

    return long_iface_name


def main():
    config_file = read_yaml_file("configuration.yaml")

    # get host ip address information from configuration file
    # this returns a dictionary which we will use to get the switch's IP
    inventory = config_file["hosts"]
    vpc_peers = config_file["vpc_peers"]

    # set up template environment
    env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True
    )

    for hostname, details in inventory.items():
        template_vars = {"mgmt_ip": details["mgmt_ip"], "vlans": config_file["vlans"]}
        for peers in vpc_peers:
            if peers["side_a"].upper() or peers["side_b"].upper() == hostname:
                template_vars["domain_id"] = peers["domain_id"]
                template_vars["system_priority"] = peers["system_priority"]
                template_vars["vrf"] = peers["vrf"]
                if hostname == peers["side_a"]:
                    template_vars["role_priority"] = "2000"
                    template_vars["peer_mgmt_ip"] = inventory[peers["side_b"]][
                        "mgmt_ip"
                    ]
                else:
                    template_vars["role_priority"] = "1000"
                    template_vars["peer_mgmt_ip"] = inventory[peers["side_a"]][
                        "mgmt_ip"
                    ]
                break

        # configure interfaces
        template_vars["interfaces"] = config_file["interfaces"][hostname]
        for name, interface_details in config_file["interfaces"][hostname].items():
            if "PORT-CHANNEL" in name.upper() or name.upper().startswith("PO"):
                template_vars["vpc_peer_link_po_num"] = re.search(r"\d+", name).group(0)
                if interface_details.get("members"):
                    template_vars["vpc_peer_link_po_members"] = []
                    for member in interface_details["members"]:
                        template_vars["vpc_peer_link_po_members"].append(
                            convert_short_iface_to_long(member).capitalize()
                        )

        template = env.get_template("config_template.j2")
        built_config = template.render(template_vars)
        print(built_config)

        # finally, let's send the config commands to the switch
        cmds_to_send = built_config.split("\n")
        response = nxapi_send_config_cmds(host=details["mgmt_ip"], cmds=cmds_to_send)
        print(json.dumps(response, indent=4))

    print("commands sent!")


if __name__ == "__main__":
    main()
