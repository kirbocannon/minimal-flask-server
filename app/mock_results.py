lldp_results = [
    {
        "hostname": "N7K-A-Pod6",
        "intended_connection": {
            "device": "N7K-A-Pod6",
            "neighbor": "N7K-B-Pod6",
            "interface": "Eth4/9",
            "neighbor_interface": "Eth4/9"
        },
        "status": "OK",
        "errors": []
    },
    {
        "hostname": "N7K-A-Pod6",
        "intended_connection": {
            "device": "N7K-A-Pod6",
            "neighbor": "N7K-B-Pod6",
            "interface": "Eth4/10",
            "neighbor_interface": "Eth4/10"
        },
        "status": "ERROR",
        "errors": [
            "ETH4/10 not found"
        ]
    },
    {
        "hostname": "N7K-A-Pod6",
        "intended_connection": {
            "device": "N7K-A-Pod6",
            "neighbor": "N5K-A-Pod6",
            "interface": "Eth4/13",
            "neighbor_interface": "Eth1/1"
        },
        "status": "OK",
        "errors": []
    },
    {
        "hostname": "N7K-A-Pod6",
        "intended_connection": {
            "device": "N7K-A-Pod6",
            "neighbor": "N5K-B-Pod6",
            "interface": "Eth4/14",
            "neighbor_interface": "Eth1/1"
        },
        "status": "ERROR",
        "errors": [
            "ETH4/14 not found"
        ]
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_connection": {
            "device": "N7K-B-Pod6",
            "neighbor": "N5K-A-Pod6",
            "interface": "Eth4/13",
            "neighbor_interface": "Eth1/2"
        },
        "status": "OK",
        "errors": []
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_connection": {
            "device": "N7K-B-Pod6",
            "neighbor": "N5K-B-Pod6",
            "interface": "Eth4/14",
            "neighbor_interface": "Eth1/2"
        },
        "status": "ERROR",
        "errors": [
            "ETH4/14 not found"
        ]
    },
    {
        "hostname": "N5K-A-Pod6",
        "intended_connection": {
            "device": "N5K-A-Pod6",
            "neighbor": "N5K-B-Pod6",
            "interface": "Eth1/3",
            "neighbor_interface": "Eth1/3",
            "state": "up"
        },
        "status": "ERROR",
        "errors": [
            "ETH1/3 not found"
        ]
    },
    {
        "hostname": "N5K-A-Pod6",
        "intended_connection": {
            "device": "N5K-A-Pod6",
            "neighbor": "N5K-B-Pod6",
            "interface": "Eth1/4",
            "neighbor_interface": "Eth1/4"
        },
        "status": "ERROR",
        "errors": [
            "ETH1/4 not found"
        ]
    }
]
vpc_results = [
    {
        "hostname": "N7K-A-Pod6",
        "intended_vpc_status": {
            "system": {
                "domain_id": 1,
                "role": "primary",
                "peer_status": "peer-ok",
                "consistency": {
                    "type1": "success",
                    "type2": "success"
                }
            },
            "peer_link": {
                "interface": "port-channel20",
                "status": "up",
                "active_vlans": [
                    1,
                    166,
                    246
                ]
            }
        },
        "current_vpc_status": {},
        "status": "OK",
        "vlans_not_found": [],
        "errors": []
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_vpc_status": {
            "system": {
                "domain_id": 1,
                "role": "secondary",
                "peer_status": "peer-ok",
                "consistency": {
                    "type1": "success",
                    "type2": "success"
                }
            },
            "peer_link": {
                "interface": "port-channel20",
                "status": "up",
                "active_vlans": [
                    1,
                    166,
                    246
                ]
            }
        },
        "current_vpc_status": {},
        "status": "OK",
        "vlans_not_found": [],
        "errors": []
    },
    {
        "hostname": "N5K-A-Pod6",
        "intended_vpc_status": {
            "system": {
                "domain_id": 2,
                "role": "primary",
                "peer_status": "peer-ok",
                "consistency": {
                    "type1": "success",
                    "type2": "success"
                }
            },
            "peer_link": {
                "interface": "port-channel20",
                "status": "up",
                "active_vlans": [
                    1,
                    166,
                    246
                ]
            }
        },
        "current_vpc_status": {},
        "status": "ERROR",
        "vlans_not_found": [
            "1",
            "166",
            "246"
        ],
        "errors": [
            "Intended vpc domain id is 2 but the current vpc domain id is 100",
            "Intended vpc peer status PEER-OK but current vpc peer status is PEER-LINK-DOWN",
            "Intended vpc type 1 consistency check is SUCCESS but current vpc type 2 consistency check is SYSERR_MCECM_COMPAT_CHK_NOT_DONE",
            "Intended vpc type 2 consistency check is SUCCESS but current vpc type 2 consistency check is SYSERR_MCECM_COMPAT_CHK_NOT_DONE",
            "Intended vpc peer link interface is PORT-CHANNEL20 but current vpc peer link interface is PORT-CHANNEL22",
            "Intended active vlans are [1, 166, 246] but current active vlans are ['-']"
        ]
    }
]
interfaces_results = [
    {
        "hostname": "N7K-A-Pod6",
        "intended_interface_status": {
            "Vlan246": {
                "state": "connected"
            }
        },
        "status": "ERROR",
        "errors": [
            "VLAN246 not found"
        ],
        "interface": "VLAN246"
    },
    {
        "hostname": "N7K-A-Pod6",
        "intended_interface_status": {
            "Vlan166": {
                "state": "connected"
            }
        },
        "status": "OK",
        "errors": [],
        "interface": "VLAN166"
    },
    {
        "hostname": "N7K-A-Pod6",
        "intended_interface_status": {
            "Vlan200": {
                "state": "connected"
            }
        },
        "status": "ERROR",
        "errors": [
            "Intended interface state for VLAN200 is CONNECTED but current interface state is DOWN"
        ],
        "interface": "VLAN200"
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_interface_status": {
            "Vlan246": {
                "state": "connected"
            }
        },
        "status": "ERROR",
        "errors": [
            "VLAN246 not found"
        ],
        "interface": "VLAN246"
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_interface_status": {
            "Vlan166": {
                "state": "connected"
            }
        },
        "status": "OK",
        "errors": [],
        "interface": "VLAN166"
    },
    {
        "hostname": "N7K-B-Pod6",
        "intended_interface_status": {
            "Vlan200": {
                "state": "connected"
            }
        },
        "status": "ERROR",
        "errors": [
            "Intended interface state for VLAN200 is CONNECTED but current interface state is DOWN"
        ],
        "interface": "VLAN200"
    }
]
