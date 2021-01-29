from expired_cert_finder.settings import Settings
from expired_cert_finder.helpers.singleton import Singleton

from os.path import isfile

def get_allowed_certs():
    settings = Settings.instance()
    allow_list_file = settings.allowed_list_filename

    return open(allow_list_file, 'r').read().splitlines() if isfile(allow_list_file) else []

@Singleton
class AllowedCerts():
    def __init__(self):
        self.allowed_certs = get_allowed_certs()