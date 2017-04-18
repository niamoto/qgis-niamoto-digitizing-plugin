# coding: utf-8

from PyQt4.QtGui import *

from digitizing_plugin.gui.ui.ui_settings import Ui_NiamotoDigitizingSettings
from digitizing_plugin import settings


class NiamotoDigitizingSettings(QDialog, Ui_NiamotoDigitizingSettings):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)
        self.niamoto_base_url.setText(settings.NIAMOTO_BASE_URL)
        self.geoserver_base_url.setText(settings.GEOSERVER_BASE_URL)

    def write_settings(self):
        settings.set_niamoto_base_url(self.niamoto_base_url.text())
        settings.set_geoserver_base_url(self.geoserver_base_url.text())

