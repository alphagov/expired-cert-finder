from expired_cert_finder.helpers.singleton import Singleton
from expired_cert_finder.defaults import EXPIRY_WINDOW, EXPIRED_CERT_LIST_FILENAME, ALLOWED_LIST_FILENAME

from expired_cert_finder.help import print_help

def val_or_default(list, key, default):
    if key not in list:
        return default
    
    return list[key]

# Update changes in print_help
@Singleton
class Settings:

    def __init__(self):
        self.ui = True
        self.save_results = False
        self.expired_only = False
        self.send_to_slack = False
        self.debug = False

        self.expiry_window = EXPIRY_WINDOW
        self.expired_cert_list_filename = EXPIRED_CERT_LIST_FILENAME
        self.allowed_list_filename = ALLOWED_LIST_FILENAME
        self.slack_webhook_url = None

    def set(self, args):
        if "help" in args:
            print_help()
            exit(0)

        self.ui = val_or_default(args, "ui", True)
        self.save_results = val_or_default(args, "save_results", False)
        self.expired_only = val_or_default(args, "expired_only", False)
        self.send_to_slack = val_or_default(args, "slack", False)
        self.debug = val_or_default(args, "debug", False)

        self.expiry_window = val_or_default(args, "expiry_window", EXPIRY_WINDOW)
        self.expired_cert_list_filename = val_or_default(args, "expired_cert_list_filename", EXPIRED_CERT_LIST_FILENAME)
        self.allowed_list_filename = val_or_default(args, "allowed_list", ALLOWED_LIST_FILENAME)
        self.slack_webhook_url = val_or_default(args, "slack_webhook_url", "")

        if self.debug:
            print("Command line arguments: " + str(args))
