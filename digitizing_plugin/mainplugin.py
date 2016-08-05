# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from requests import ConnectionError

from digitizing_plugin.ui.massifs_dock import Ui_MassifTableWidget
from digitizing_plugin import settings
from digitizing_plugin import fetch_data
from utils import log, construct_wfs_uri


GEOSERVER_BASE_URL = settings.GEOSERVER_BASE_URL
NIAMOTO_WFS_URL = GEOSERVER_BASE_URL + '/niamoto/wfs'
DIGITIZING_WFS_URL = GEOSERVER_BASE_URL + '/digitizing/wfs'


class DigitizingPlugin(object):

    CONNECTION_FAILED_TEXT = \
        u"""
        Ahou pardon! La connection au serveur a échoué, vérifiez votre,
        connection internet. Si malgré ça le problème persiste, contactez les
        développeurs de niamoto.
        """
    RETRY_CONNECTION_TEXT = u"Retenter la connection"

    def __init__(self, iface):
        self.iface = iface
        self.massifs_dock = QDockWidget("Digitalisation")
        self.massif_table_widget = None
        self.connection_failed_widget = None
        self.retry_button = None
        self.init_connection_failed_widget()
        self.init_massif_table_widget()

    def init_massif_table_widget(self):
        try:
            self.retry_button.setEnabled(False)
            self.massif_table_widget = MassifTableWidget(self.iface)
            self.massifs_dock.setWidget(self.massif_table_widget)
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.massifs_dock.setWidget(self.connection_failed_widget)

    def init_connection_failed_widget(self):
        label = QLabel(self.CONNECTION_FAILED_TEXT)
        self.retry_button = QPushButton(self.RETRY_CONNECTION_TEXT)
        self.retry_button.clicked.connect(self.init_massif_table_widget)
        layout = QVBoxLayout()
        spacer = QSpacerItem(
            10, 10,
            QSizePolicy.MinimumExpanding,
            QSizePolicy.Expanding
        )
        layout.addItem(spacer)
        layout.addWidget(label)
        layout.addWidget(self.retry_button)
        layout.addItem(QSpacerItem(spacer))
        self.connection_failed_widget = QWidget()
        self.connection_failed_widget.setLayout(layout)

    def initGui(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.massifs_dock)

    def run(self):
        self.massifs_dock.show()

    def unload(self):
        pass

    def get_massif_id(self, massif_key_name):
        return self.massif_table_widget.massif_map[massif_key_name]

    def get_operator_id(self):
        cb = self.massif_table_widget.user_combobox
        return cb.itemData(cb.currentIndex(), Qt.UserRole)


class MassifTableWidget(QWidget, Ui_MassifTableWidget):

    STATUS_LABELS = {
        0: u"Non digitalisé",
        1: u"En cours de digitalisation",
        2: u"A valider",
    }

    def __init__(self, iface, parent=None):
        super(MassifTableWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.assignations = fetch_data.fetch_massif_assignations()
        self.all_users = self.get_user_map(fetch_data.fetch_users())
        self.massif_map = self.get_massif_map(self.assignations)
        self.populate_table()
        self.populate_combobox()
        self.add_massif_button.clicked.connect(self.add_layer_group)
        self.treeWidget.currentItemChanged.connect(self.tree_clicked)
        self.treeWidget.setCurrentIndex(QModelIndex())
        self.add_massif_button.setEnabled(False)
        self.user_combobox.currentIndexChanged.connect(self.operator_changed)

    def populate_table(self):
        rows = list()
        for a in self.assignations:
            item = QTreeWidgetItem()
            item.setData(0, Qt.UserRole, a)
            item.setText(0, unicode(a['massif_key_name']))
            operator_full_name = self.all_users[a['operator']]['full_name']
            item.setText(1, unicode(operator_full_name))
            item.setText(2, unicode(self.STATUS_LABELS[a['status']]))
            rows.append(item)
        self.treeWidget.addTopLevelItems(rows)

    def populate_combobox(self):
        users = fetch_data.fetch_users(only_team=True)
        index = None
        for i, u in enumerate(users):
            self.user_combobox.addItem(u['full_name'], u['id'])
            if settings.LAST_OPERATOR is not None:
                if u['full_name'] == settings.LAST_OPERATOR:
                    index = i
        if index is not None:
            self.user_combobox.setCurrentIndex(index)

    def operator_changed(self):
        operator = self.user_combobox.currentText()
        settings.SETTINGS['LAST_OPERATOR'] = unicode(operator)
        settings.write_settings()

    @staticmethod
    def get_user_map(user_list):
        user_map = dict()
        for u in user_list:
            user_map[u['id']] = u
        return user_map

    @staticmethod
    def get_massif_map(assignations):
        massif_map = dict()
        for a in assignations:
            massif_map[a['massif_key_name']] = a['massif_id']
        return massif_map

    def add_layer_group(self):
        # Get selected massif name
        selected_massif = self.treeWidget.currentItem()
        massif_key_name = selected_massif.text(0)
        assignation = selected_massif.data(0, Qt.UserRole)
        # Create group
        root = QgsProject.instance().layerTreeRoot()
        group = root.insertGroup(0, massif_key_name)
        # Add digitizing problems
        pb_layer = self.get_digitizing_problem_layer(assignation)
        pb_layer.loadSldStyle(settings.DIGITIZING_PROBLEM_SLD_STYLE_PATH)
        pb_layer.editFormConfig().setUiForm(settings.PROBLEM_FORM_PATH)
        pb_layer.editFormConfig().setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
        pb_layer.editFormConfig().setInitFilePath(settings.PROBLEM_FORM_INIT_PATH)
        pb_layer.editFormConfig().setInitFunction(settings.PROBLEM_FORM_INIT_FUNCTION)
        QgsMapLayerRegistry.instance().addMapLayer(pb_layer, False)
        pb_node = QgsLayerTreeLayer(pb_layer)
        group.addChildNode(pb_node)
        # Add forest3k
        f3k_layer = self.get_forest_area_3k_layer(assignation)
        f3k_layer.loadSldStyle(settings.FOREST_AREA_3K_SLD_STYLE_PATH)
        f3k_layer.editFormConfig().setUiForm(settings.FOREST_FORM_PATH)
        f3k_layer.editFormConfig().setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
        f3k_layer.editFormConfig().setInitFilePath(settings.FOREST_FORM_INIT_PATH)
        f3k_layer.editFormConfig().setInitFunction(settings.FOREST_FORM_INIT_FUNCTION)
        QgsMapLayerRegistry.instance().addMapLayer(f3k_layer, False)
        f3k_node = QgsLayerTreeLayer(f3k_layer)
        group.addChildNode(f3k_node)
        # Add forest30k
        f30k_layer = self.get_forest_area_30k_layer(assignation)
        f30k_layer.loadSldStyle(settings.FOREST_AREA_30K_SLD_STYLE_PATH)
        QgsMapLayerRegistry.instance().addMapLayer(f30k_layer, False)
        f30k_node = QgsLayerTreeLayer(f30k_layer)
        f30k_node.setVisible(False)
        group.addChildNode(f30k_node)
        # Add massif node
        massif_layer = self.get_massif_layer(massif_key_name)
        massif_layer.loadSldStyle(settings.MASSIF_SLD_STYLE_PATH)
        QgsMapLayerRegistry.instance().addMapLayer(massif_layer, False)
        massif_node = QgsLayerTreeLayer(massif_layer)
        group.addChildNode(massif_node)

    def tree_clicked(self):
        self.add_massif_button.setEnabled(True)

    def get_massif_layer(self, massif_key_name):
        log(u"{} - Adding massif wfs layer".format(massif_key_name))
        uri = construct_wfs_uri(
            NIAMOTO_WFS_URL,
            'niamoto:niamoto_data_massif',
            version='1.0.0',
            srsname='EPSG:4326',
            filter="key_name='{}'".format(massif_key_name)
        )
        log(uri)
        return QgsVectorLayer(
            uri,
            "Massif - {}".format(massif_key_name),
            "WFS"
        )

    def get_forest_area_30k_layer(self, assignation):
        massif_key_name = assignation['massif_key_name']
        massif_id = assignation['massif_id']
        log(u"{} - Adding forest area 30k wfs layer".format(massif_key_name))
        uri = construct_wfs_uri(
            NIAMOTO_WFS_URL,
            'niamoto:forest_digitizing_forestfragment30k',
            version='1.0.0',
            srsname='EPSG:4326',
            filter='massif_id={}'.format(massif_id)
        )
        log(uri)
        return QgsVectorLayer(
            uri,
            "Forest 30k - {}".format(massif_key_name),
            "WFS"
        )

    def get_forest_area_3k_layer(self, assignation):
        massif_key_name = assignation['massif_key_name']
        massif_id = assignation['massif_id']
        log(u"{} - Adding forest area 3k wfs layer".format(massif_key_name))
        uri = construct_wfs_uri(
            DIGITIZING_WFS_URL,
            'digitizing:forest_digitizing_forestfragment3k',
            version='1.0.0',
            srsname='EPSG:4326',
            filter='massif_id={}'.format(massif_id)
        )
        log(uri)
        return QgsVectorLayer(
            uri,
            "Forest 3k - {}".format(massif_key_name),
            "WFS"
        )

    def get_digitizing_problem_layer(self, assignation):
        massif_key_name = assignation['massif_key_name']
        massif_id = assignation['massif_id']
        log(u"{} - Adding problems wfs layer".format(massif_key_name))
        uri = construct_wfs_uri(
            DIGITIZING_WFS_URL,
            'digitizing:forest_digitizing_digitizingproblem',
            version='1.0.0',
            srsname='EPSG:4326',
            filter='massif_id={}'.format(massif_id)
        )
        log(uri)
        return QgsVectorLayer(
            uri,
            "Digitizing Problems - {}".format(massif_key_name),
            "WFS"
        )
