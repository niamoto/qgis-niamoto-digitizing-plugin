# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'digitizing_plugin/ui/settings.ui'
#
# Created: Mon Apr 17 18:36:38 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_NiamotoDigitizingSettings(object):
    def setupUi(self, NiamotoDigitizingSettings):
        NiamotoDigitizingSettings.setObjectName(_fromUtf8("NiamotoDigitizingSettings"))
        NiamotoDigitizingSettings.resize(415, 119)
        self.verticalLayout_2 = QtGui.QVBoxLayout(NiamotoDigitizingSettings)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(NiamotoDigitizingSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(NiamotoDigitizingSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NiamotoDigitizingSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NiamotoDigitizingSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(NiamotoDigitizingSettings)

    def retranslateUi(self, NiamotoDigitizingSettings):
        NiamotoDigitizingSettings.setWindowTitle(_translate("NiamotoDigitizingSettings", "Niamoto Digitizing - Settings", None))

