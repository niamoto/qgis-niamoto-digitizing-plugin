# coding: utf-8

import uuid
from datetime import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qgis
from qgis.core import *


def log(msg):
    QgsMessageLog.logMessage(msg, 'digitizing_plugin')


dialog = None
layer = None
feature = None

uuid_edit = None
created = None
created_by = None
modified = None
modified_by = None
massif_id = None
comments = None


def initForm(_dialog, _layer, _feature):
    # To prevent qgis throwing an error when looking the whole attr. table
    try :
        _feature['id']
    except:
        return
    global dialog, layer, feature
    dialog = _dialog
    layer = _layer
    feature = _feature
    global uuid_edit, created, created_by, modified, modified_by, massif_id, \
        comments
    dialog.findChild(QGroupBox, 'hideit').hide()
    # Retrieve massif_id and operator_id from digitizing plugin
    massif_id_val = get_massif_id(layer)
    operator_id = get_operator_id()
    # log(u"massif_id: {}".format(massif_id_val))
    # log(u"operator_id: {}".format(operator_id))
    # Get fields
    uuid_edit = dialog.findChild(QLineEdit, 'uuid')
    created_by = dialog.findChild(QLineEdit, 'created_by_id')
    modified_by = dialog.findChild(QLineEdit, 'modified_by_id')
    comments = dialog.findChild(QLineEdit, 'comments')
    created = dialog.findChild(QLineEdit, 'created')
    modified = dialog.findChild(QLineEdit, 'modified')
    massif_id_widget = dialog.findChild(QLineEdit, 'massif_id')
    if isUpdating():
        modified_by.setText(unicode(operator_id))
        modified.setText(unicode(datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))
    else:
        created_by.setText(unicode(operator_id))
        uuid_edit.setText(unicode(uuid.uuid1()))
        massif_id_widget.setText(unicode(massif_id_val))
        created.setText(unicode(datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))


def isUpdating():
    if feature['id'] is not None:
        return True
    return False


def get_massif_id(_layer):
    massif_key_name = _layer.name().split(" - ")[1]
    digitizing_plugin = qgis.utils.plugins['digitizing_plugin']
    return digitizing_plugin.get_massif_id(massif_key_name)


def get_operator_id():
    digitizing_plugin = qgis.utils.plugins['digitizing_plugin']
    return digitizing_plugin.get_operator_id()
