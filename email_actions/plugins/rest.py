import requests
import logging

from email_actions.config import read_config_plugin

PLUGIN_NAME = 'rest'


def rest_notify(filter_name, msg_from, msg_to, msg_subject, msg_content):
    plugin_cfg = read_config_plugin(filter_name, PLUGIN_NAME)

    config = {
        'endpoint': None,
        'headers': {},
        'data': {},
    }
    for key in plugin_cfg:
        config[key] = plugin_cfg[key]

    config['data']['filter'] = filter_name
    config['data']['message'] = {
        'from': msg_from,
        'to': msg_to,
        'subject': msg_subject,
        'body': msg_content
    }

    if not config['endpoint']:
        logging.debug("Skipping action because no REST endpoint is set.")
    logging.debug("Sending REST request to %s" % (config['endpoint']))
    try:
        r = requests.post(config['endpoint'], headers=config['headers'], json=config['data'])
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error while sending REST request: %s" % (e))
