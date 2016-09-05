# coding: utf-8

import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import requests
from requests import ConnectionError

from digitizing_plugin.ui.authentication_widget import Ui_AuthenticationWidget
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
        self.authentication_widget = None
        self.session = None
        self.retry_button = None
        self.init_authentication_widget()
        self.init_connection_failed_widget()
        self.authenticate()

    def authenticate(self):
        self.authentication_widget.status_label.setText(u"")
        if self.session is None:
            self.authentication_widget.login_edit.setText(u"")
            self.authentication_widget.password_edit.setText(u"")
            self.massifs_dock.setWidget(self.authentication_widget)
        else:
            self.connect()

    def connect(self):
        username = self.authentication_widget.login_edit.text()
        password = self.authentication_widget.password_edit.text()
        if not username or not password:
            t = u"Les informations de connexion sont incorrectes."
            st = u"color: red;"
            self.authentication_widget.status_label.setStyleSheet(st)
            self.authentication_widget.status_label.setText(t)
            self.session = None
            return
        try:
            data = {
                u"grant_type": u"password",
                u"username": username,
                u"password": password,
            }
            auth = (settings.OAUTH2_CLIENT_ID, settings.OAUTH2_CLIENT_SECRET)
            r = requests.post(
                settings.NIAMOTO_OAUTH2_TOKEN_URL,
                data=data, auth=auth
            )
            if r.status_code == requests.codes.ok:
                token = json.loads(r.text)
                self.session = {
                    u"token_type": token[u"token_type"],
                    u"access_token": token[u"access_token"],
                    u"refresh_token": token[u"refresh_token"]
                }
                self.get_whoami()
                t = u"Authentification réussie, chargement des données..."
                st = u"color: green;"
                self.authentication_widget.status_label.setStyleSheet(st)
                self.authentication_widget.status_label.setText(t)
                QApplication.processEvents()
                self.init_massif_table_widget()
            elif r.status_code == requests.codes.unauthorized:
                t = u"Les informations de connexion sont incorrectes."
                st = u"color: red;"
                self.authentication_widget.status_label.setStyleSheet(st)
                self.authentication_widget.status_label.setText(t)
                self.session = None
            else:
                self.session = None
                r.raise_for_status()
        except (ConnectionError, Exception):
            self.session = None
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.massifs_dock.setWidget(self.connection_failed_widget)

    def get_whoami(self):
        try:
            headers = {
                u"Authorization": u"{} {}".format(
                    self.session[u"token_type"],
                    self.session[u"access_token"],
                )
            }
            r = requests.get(
                u"{}whoami/".format(settings.NIAMOTO_REST_BASE_URL),
                headers=headers
            )
            r.raise_for_status()
            if r.status_code == requests.codes.ok:
                whoami = json.loads(r.text)
                self.session[u"userid"] = whoami[u"id"]
                self.session[u"useremail"] = whoami[u"email"]
                self.session[u"username"] = whoami[u"username"]
            elif r.status_code == requests.codes.unauthorized:
                self.authentication_widget.status_label.setText(
                    u"""
                    Les informations de connexon sont incorrectes.
                    """
                )
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.massifs_dock.setWidget(self.connection_failed_widget)

    def logout(self):
        self.session = None
        self.authenticate()

    def init_massif_table_widget(self):
        try:
            self.retry_button.setEnabled(False)
            self.massif_table_widget = MassifTableWidget(self.iface, self.session)
            self.massif_table_widget.logout_button.clicked.connect(self.logout)
            self.massifs_dock.setWidget(self.massif_table_widget)
        except (ConnectionError, Exception):
            log(u"Connection failed!")
            self.retry_button.setEnabled(True)
            self.massifs_dock.setWidget(self.connection_failed_widget)

    def init_connection_failed_widget(self):
        label = QLabel(self.CONNECTION_FAILED_TEXT)
        self.retry_button = QPushButton(self.RETRY_CONNECTION_TEXT)
        self.retry_button.clicked.connect(self.authenticate)
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

    def init_authentication_widget(self):
        self.authentication_widget = AuthenticationWidget()
        self.authentication_widget.connect_button.clicked.connect(self.connect)

    def initGui(self):
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.massifs_dock)

    def run(self):
        self.massifs_dock.show()

    def unload(self):
        pass

    def get_massif_id(self, massif_key_name):
        return self.massif_table_widget.massif_map[massif_key_name]

    def get_operator_id(self):
        return self.session[u"userid"]


class AuthenticationWidget(QWidget, Ui_AuthenticationWidget):

    def __init__(self, parent=None):
        super(AuthenticationWidget, self).__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Enter:
                self.connect_button.click()


class MassifTableWidget(QWidget, Ui_MassifTableWidget):

    STATUS_LABELS = {
        0: u"Non digitalisé",
        1: u"En cours de digitalisation",
        2: u"A valider",
    }

    def __init__(self, iface, session, parent=None):
        super(MassifTableWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.session = session
        self.username_label.setText(self.session[u"username"])
        self.assignations = fetch_data.fetch_massif_assignations(self.session)
        self.massif_map = self.get_massif_map(self.assignations)
        self.populate_table()
        self.add_massif_button.clicked.connect(self.add_layer_group)
        self.treeWidget.currentItemChanged.connect(self.tree_clicked)
        self.treeWidget.doubleClicked.connect(self.add_layer_group)
        self.treeWidget.setCurrentIndex(QModelIndex())
        self.add_massif_button.setEnabled(False)

    def populate_table(self):
        rows = list()
        for a in self.assignations:
            item = QTreeWidgetItem()
            item.setData(0, Qt.UserRole, a)
            item.setText(0, unicode(a['massif_key_name']))
            item.setText(1, unicode(a['operator_full_name']))
            item.setText(2, unicode(self.STATUS_LABELS[a['status']]))
            rows.append(item)
        self.treeWidget.addTopLevelItems(rows)

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
        pb_layer.committedFeaturesAdded.connect(lambda: self.update_layer(pb_layer))

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
        f3k_layer.committedFeaturesAdded.connect(lambda: self.update_layer(f3k_layer))

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

    @staticmethod
    def update_layer(layer):
        layer.reload()
        layer.dataProvider().forceReload()
        layer.triggerRepaint()
        log("New feature added, reload triggered")

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
