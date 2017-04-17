# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from digitizing_plugin.gui.ui.ui_settings import Ui_NiamotoDigitizingSettings


class NiamotoDigitizingSettings(QDialog, Ui_NiamotoDigitizingSettings):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)

