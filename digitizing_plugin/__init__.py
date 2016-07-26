# coding: utf-8

import os


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))


def classFactory(iface):
    from mainplugin import DigitizingPlugin
    return DigitizingPlugin(iface)
