# coding: utf-8

from qgis.core import *


def log(msg):
    QgsMessageLog.logMessage(msg, 'digitizing_plugin')


def construct_wfs_uri(url, typename, **kwargs):
    params = {
        'url': url,
        'typename': typename,
        'request': 'GetFeature',
        'user': 'digitizer',
        'password': 'niamoto_digitizer'
    }
    params.update(kwargs)
    return ' '.join(['{}="{}"'.format(k, v) for k, v in params.items()])
