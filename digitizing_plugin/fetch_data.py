# coding: utf-8

import json
import urlparse

import requests

from digitizing_plugin.utils import log
from digitizing_plugin import settings


NIAMOTO_REST_BASE_URL = settings.NIAMOTO_REST_BASE_URL


def fetch_massif_assignations():
    """
    Fetch the massif assignation data from niamoto's rest api.
    """
    log(u"Fetching massif assignation data from niamoto server...")
    session = requests.Session()
    url = urlparse.urljoin(
        NIAMOTO_REST_BASE_URL,
        u"massif_assignation"
    )
    r = session.get(url)
    assignations = json.loads(r.text)
    log(u"massif assignation data fetched!")
    return assignations


def fetch_users(only_team=False):
    """
    Fetch the user list from niamoto's rest api.
    """
    log(u"Fetching user data from niamoto server...")
    session = requests.Session()
    url = urlparse.urljoin(
        NIAMOTO_REST_BASE_URL,
        u"user"
    )
    if only_team:
        url = urlparse.urljoin(
            url,
            u"?only_team=true"
        )
    r = session.get(url)
    users = json.loads(r.text)
    log(u"user data fetched!")
    return users
