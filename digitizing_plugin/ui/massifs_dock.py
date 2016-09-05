# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'digitizing_plugin/ui/massifs_dock.ui'
#
# Created: Mon Sep  5 14:39:42 2016
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
        self.username_label = QtGui.QLabel(MassifTableWidget)
        self.username_label.setStyleSheet(_fromUtf8("font: 75 14pt \"Cantarell\";\n"
""))
        self.username_label.setText(_fromUtf8(""))
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        self.username_label.setObjectName(_fromUtf8("username_label"))
        self.horizontalLayout.addWidget(self.username_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.logout_button = QtGui.QPushButton(MassifTableWidget)
        self.logout_button.setStyleSheet(_fromUtf8("color: red;"))
        self.logout_button.setFlat(True)
        self.logout_button.setObjectName(_fromUtf8("logout_button"))
        self.horizontalLayout.addWidget(self.logout_button)
        self.horizontalLayout.setStretch(1, 1)
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
        self.logout_button.setText(_translate("MassifTableWidget", "Déconnexion", None))

