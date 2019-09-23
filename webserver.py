import os
import json
import pynetbox
import app.config as config
from collections import defaultdict
from flask import Flask, render_template


app = Flask(
    __name__,
    static_folder=os.path.join(config.BASEDIR, "static"),
    template_folder=os.path.join(config.BASEDIR, "templates"),
)


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route("/treemap")
def treemap():
    nb = pynetbox.api(
        'http://localhost:8080',
        token='db451c6b1d452f82b9b35cf1cdc1088a400938ac',
    )

    treemap = {
        "name": "netbox",
        "children": [
            {
                "name": "site",
                "children": []
            }
        ]
    }

    sites = nb.dcim.sites.all()
    devices = nb.dcim.devices.all()

    ss = {}
    for site in sites:
        ss[site.name] = {
            "rack_total": site.rack_count or 0,
            "device_total": 0,
            "role_totals": defaultdict(lambda: 0)
        }

        for device in devices:
            if device.site.name.lower() == site.name.lower():
                ss[site.name]["device_total"] += 1
                ss[site.name]["role_totals"][str(device.device_role)] += 1

        # build child node for tree map
        site_child = {
            "name": site.name,
            "children": [
                {
                    "name": "device",
                    "children": [
                        {"name": "Rack", "size": ss[site.name]['rack_total']}
                        #{"name": "DeviceTotal", "size": ss[site.name]['device_total']}
                    ]
                }
            ]
        }

        for role, count in ss[site.name]["role_totals"].items():
            site_child["children"][0]["children"].append(
                {
                    "name": role,
                    "size": count
                }
            )

        treemap["children"][0]["children"].append(site_child)

    with open(os.path.join(
            config.BASEDIR,
            'static',
            'netbox-treemap-data.json'),
            'w+') as f:
        json.dump(treemap, f, indent=2)

    return render_template('treemap.html')


if __name__ == '__main__':

    mode = 'development'

    if mode == 'development':
        app.config.from_object(config.Development)
        app.run()
    elif mode == 'production':
        app.config.from_object(config.Production)
        app.run()
