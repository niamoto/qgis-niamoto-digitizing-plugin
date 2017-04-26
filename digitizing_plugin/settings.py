# coding: utf-8

import os
import json

from digitizing_plugin import PACKAGE_ROOT


SETTINGS_FILE = os.path.join(PACKAGE_ROOT, "settings.json")
SETTINGS = dict()


def load_settings():
    global SETTINGS
    if not os.path.exists(SETTINGS_FILE):
        write_settings()
    with open(SETTINGS_FILE, 'r') as settings_file:
        SETTINGS = json.load(settings_file)


def write_settings():
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump(SETTINGS, settings_file)


load_settings()


NIAMOTO_BASE_URL = SETTINGS.get(
    "NIAMOTO_REST_BASE_URL",
    u"https://niamoto.io/"
)
NIAMOTO_REST_BASE_URL = NIAMOTO_BASE_URL + u"api/1.0/"


def set_niamoto_base_url(value):
    global SETTINGS, \
        NIAMOTO_BASE_URL, \
        NIAMOTO_REST_BASE_URL,\
        NIAMOTO_OAUTH2_TOKEN_URL
    NIAMOTO_BASE_URL = value
    NIAMOTO_REST_BASE_URL = NIAMOTO_BASE_URL + u"api/1.0/"
    NIAMOTO_OAUTH2_TOKEN_URL = NIAMOTO_BASE_URL + u"o/token/"
    SETTINGS['NIAMOTO_BASE_URL'] = value
    write_settings()


GEOSERVER_BASE_URL = SETTINGS.get(
    "GEOSERVER_BASE_URL",
    u"https://geo.niamoto.io/geoserver/"
)
NIAMOTO_WFS_URL = GEOSERVER_BASE_URL + u'niamoto/wfs/'
DIGITIZING_WFS_URL = GEOSERVER_BASE_URL + u'digitizing/wfs/'


def set_geoserver_base_url(value):
    global SETTINGS,\
        GEOSERVER_BASE_URL,\
        NIAMOTO_WFS_URL,\
        DIGITIZING_WFS_URL
    GEOSERVER_BASE_URL = value
    NIAMOTO_WFS_URL = GEOSERVER_BASE_URL + u'niamoto/wfs/'
    DIGITIZING_WFS_URL = GEOSERVER_BASE_URL + u'digitizing/wfs/'
    SETTINGS['GEOSERVER_BASE_URL'] = value
    write_settings()


STATIC_PATH = SETTINGS.get(
    "STATIC_PATH",
    os.path.join(PACKAGE_ROOT, "static")
)


# ================ #
# User preferences #
# ================ #

LAST_OPERATOR = SETTINGS.get(
    "LAST_OPERATOR",
    None,
)


# ================ #
# SLD static files #
# ================ #

STYLE_PATH = SETTINGS.get(
    "STYLE_PATH",
    os.path.join(STATIC_PATH, "styles")
)

MASSIF_SLD_STYLE_PATH = SETTINGS.get(
    "MASSIF_SLD_STYLE_PATH",
    os.path.join(STYLE_PATH, "massif_style.sld")
)

FOREST_AREA_30K_SLD_STYLE_PATH = SETTINGS.get(
    "FOREST_AREA_30K_SLD_STYLE_PATH",
    os.path.join(STYLE_PATH, "forest_area_30k_style.sld")
)

FOREST_AREA_3K_SLD_STYLE_PATH = SETTINGS.get(
    "FOREST_AREA_3K_SLD_STYLE_PATH",
    os.path.join(STYLE_PATH, "forest_area_3k_style.sld")
)

DIGITIZING_PROBLEM_SLD_STYLE_PATH = SETTINGS.get(
    "DIGITIZING_PROBLEM_SLD_STYLE_PATH",
    os.path.join(STYLE_PATH, "digitizing_problem_style.sld")
)

# ==================== #
# Ui form static files #
# ==================== #

FORM_PATH = SETTINGS.get(
    "FORM_PATH",
    os.path.join(STATIC_PATH, "forms")
)

FOREST_FORM_PATH = SETTINGS.get(
    "FOREST_FORM_PATH",
    os.path.join(FORM_PATH, "forest_form.ui")
)

PROBLEM_FORM_PATH = SETTINGS.get(
    "PROBLEM_FORM_PATH",
    os.path.join(FORM_PATH, "problem_form.ui")
)

# ================================ #
# Python init scripts static files #
# ================================ #

FORM_INIT_PATH = SETTINGS.get(
    "FORM_INIT_PATH",
    os.path.join(STATIC_PATH, "form_init_scripts")
)

FOREST_FORM_INIT_PATH = SETTINGS.get(
    "FOREST_FORM_INIT_PATH",
    os.path.join(FORM_INIT_PATH, "forest_form_init.py")
)

FOREST_FORM_INIT_FUNCTION = SETTINGS.get(
    "FOREST_FORM_INIT_FUNCTION",
    "initForm"
)

PROBLEM_FORM_INIT_PATH = SETTINGS.get(
    "PROBLEM_FORM_INIT_PATH",
    os.path.join(FORM_INIT_PATH, "problem_form_init.py")
)

PROBLEM_FORM_INIT_FUNCTION = SETTINGS.get(
    "PROBLEM_FORM_INIT_FUNCTION",
    "initForm"
)

# =============== #
# OAUTH2 settings #
# =============== #

NIAMOTO_OAUTH2_TOKEN_URL = NIAMOTO_BASE_URL + u"o/token/"

OAUTH2_CLIENT_ID = SETTINGS.get(
    "OAUTH2_CLIENT_ID",
    "B2hnMW13ZZuzpDglmfjAJHfos7pDat4IlsJFYBMi"
)

OAUTH2_CLIENT_SECRET = SETTINGS.get(
    "OAUTH2_CLIENT_SECRET",
    "Z5cR3DJLzyMM0Qaxs3lLU1GOqdrFPb4HDkghAcPUU556WuZJ6EjA8Cd6KHORhuliPAHwunYe5IFrmoCPGbmU7tpm57pJuisOBBBF1Yqgt5hZuIZhq9JT6KcK73sovzD6"
)
