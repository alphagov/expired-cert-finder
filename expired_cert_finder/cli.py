import sys
from sys import exit as sys_exit
from signal import signal, SIGINT
from datetime import datetime, timedelta

from fire import Fire
from progress.bar import IncrementalBar
from progress.counter import Counter

from expired_cert_finder.settings import Settings
from expired_cert_finder.scanner import scan_file_for_certificate
from expired_cert_finder.defaults import PWD
from expired_cert_finder.fs import find_files
from expired_cert_finder.save import save_file
from expired_cert_finder.slack import send_to_slack


# varags: is the command line arguments not starting with --
# args: is the command line arguments starting with --
def cli_runner(*varags, **args):
    signal(SIGINT, ctrl_c_handler)  # Handle Ctrl + C

    settings = Settings.instance()
    settings.set(args)

    if settings.debug:
        print("Command line inputs: " + str(varags))

    counter = None
    if settings.ui:
        counter = Counter('Discovering Files: ')

    def counter_func():
        if counter != None:
            counter.next()

    files_to_process = []
    if len(varags) > 0:
        for arg in varags:
            files_to_process += find_files(arg, counter_func)
    else:
        if settings.debug:
            print("No inputs provided, Scanning local directory")
        files_to_process = find_files(PWD, counter_func)

    if counter:
        counter.finish()

    problematic_certs = process_certs(files_to_process, settings)

    if settings.save_results:
        save_file(problematic_certs)

    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    expired_certs = [cert for cert in problematic_certs
                     if cert['expiry_datetime'] < today]

    if len(expired_certs) > 0:
        print("** The following certs have expired!! **")
        for cert in expired_certs:
            print(cert['message'])

    next_working_day = today + timedelta(1)
    if today.weekday() == 4:
        next_working_day = today + timedelta(3)
    immediate_action = [cert for cert in problematic_certs
                        if today < cert['expiry_datetime'] < next_working_day]

    if len(immediate_action) > 0:
        print("The following certs need IMMEDIATE ACTION")
        for cert in immediate_action:
            print(cert['message'])

    next_week = today + timedelta(7)
    next_7_days = [cert for cert in problematic_certs
                   if next_working_day < cert['expiry_datetime'] < next_week]

    if len(next_7_days) > 0:
        print("The following certs expire in the next 7 days")
        for cert in next_7_days:
            print(cert['message'])

    remaining = [cert for cert in problematic_certs if cert['expiry_datetime'] > next_week]
    if len(remaining) > 0:
        print("The following certs expire in more than 7 days time")
        for cert in remaining:
            print(cert['message'])

    if settings.send_to_slack and len(problematic_certs) > 0:
        send_to_slack(expired_certs, immediate_action, next_7_days, remaining)


def process_certs(files_to_process, settings):
    no_files = len(files_to_process)

    if settings.debug:
        print("Number of files found: %s" % no_files)

    progress = None
    if settings.ui:
        progress = IncrementalBar('Scanning Expired Certificates', max=no_files)

    problematic_certs = []
    for file in files_to_process:
        problematic_certs += scan_file_for_certificate(file, settings.expired_only, settings.debug)
        if progress != None:
            progress.next()

    if progress is not None:
        progress.finish()

    return sorted(problematic_certs, key=lambda k: (k['not_after'], k['subject']))


def ctrl_c_handler(sig, frame):
    sys_exit(0)


def run():
    Fire(cli_runner)
