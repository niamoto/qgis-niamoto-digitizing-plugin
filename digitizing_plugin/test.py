# coding: utf-8

import sys

from PyQt4.QtGui import *
from digitizing_plugin.mainplugin import MassifTableWidget
from digitizing_plugin.mainplugin import AuthenticationWidget


def main(args):
    app = QApplication(sys.argv)
    auth_widget = AuthenticationWidget(None)
    auth_widget.show()
    taxon_tree_widget = MassifTableWidget(None)
    taxon_tree_widget.show()
    app.exec_()


if __name__ == '__main__':
    print("Start")

    main(sys.argv)
