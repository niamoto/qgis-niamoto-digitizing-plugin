# coding: utf-8

from qgis.core import *


def log(msg):
    QgsMessageLog.logMessage(msg, 'digitizing_plugin')


def get_ogc_equal_filter(property_name, value):
    ogc_filter = \
        '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">' + \
        '<ogc:PropertyIsEqualTo>' + \
        '<ogc:PropertyName>{}</ogc:PropertyName>' + \
        '<ogc:Literal>{}</ogc:Literal>' + \
        '</ogc:PropertyIsEqualTo>' + \
        '</ogc:Filter>'
    return ogc_filter.format(property_name, str(value))
