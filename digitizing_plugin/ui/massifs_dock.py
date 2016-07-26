# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/massifs_dock.ui'
#
# Created: Fri Jul 22 11:59:47 2016
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

class Ui_MassifTableWidget(object):
    def setupUi(self, MassifTableWidget):
        MassifTableWidget.setObjectName(_fromUtf8("MassifTableWidget"))
        MassifTableWidget.resize(662, 624)
        self.verticalLayout = QtGui.QVBoxLayout(MassifTableWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget = QtGui.QTreeWidget(MassifTableWidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.verticalLayout.addWidget(self.treeWidget)
        self.add_massif_button = QtGui.QPushButton(MassifTableWidget)
        self.add_massif_button.setObjectName(_fromUtf8("add_massif_button"))
        self.verticalLayout.addWidget(self.add_massif_button)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(MassifTableWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.user_combobox = QtGui.QComboBox(MassifTableWidget)
        self.user_combobox.setObjectName(_fromUtf8("user_combobox"))
        self.horizontalLayout.addWidget(self.user_combobox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MassifTableWidget)
        QtCore.QMetaObject.connectSlotsByName(MassifTableWidget)

    def retranslateUi(self, MassifTableWidget):
        MassifTableWidget.setWindowTitle(_translate("MassifTableWidget", "Form", None))
        self.treeWidget.headerItem().setText(0, _translate("MassifTableWidget", "Massif", None))
        self.treeWidget.headerItem().setText(1, _translate("MassifTableWidget", "Opérateur", None))
        self.treeWidget.headerItem().setText(2, _translate("MassifTableWidget", "Status", None))
        self.add_massif_button.setText(_translate("MassifTableWidget", "Ajouter les couches du massif", None))
        self.label.setText(_translate("MassifTableWidget", "Opérateur actuel:", None))

