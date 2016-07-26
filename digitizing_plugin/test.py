# coding: utf-8

import sys

from PyQt4.QtGui import *
from digitizing_plugin.mainplugin import MassifTableWidget


def main(args):
    app = QApplication(sys.argv)
    taxon_tree_widget = MassifTableWidget(None)
    taxon_tree_widget.show()
    app.exec_()


if __name__ == '__main__':
    print("Start")

    main(sys.argv)
