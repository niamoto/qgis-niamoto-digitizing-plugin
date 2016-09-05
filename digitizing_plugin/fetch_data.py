# coding: utf-8

import json
import urlparse

import requests

from digitizing_plugin.utils import log
from digitizing_plugin import settings


NIAMOTO_REST_BASE_URL = settings.NIAMOTO_REST_BASE_URL


def fetch_massif_assignations(session):
    """
    Fetch the massif assignation data from niamoto's rest api.
    """
    log(u"Fetching massif assignation data from niamoto server...")
    url = urlparse.urljoin(
        NIAMOTO_REST_BASE_URL,
        u"forest_digitizing/massif_assignation/"
    )
    headers = {
        u"Authorization": u"{} {}".format(
            session[u"token_type"],
            session[u"access_token"],
        )
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    assignations = json.loads(r.text)
    log(u"massif assignation data fetched!")
    return assignations
