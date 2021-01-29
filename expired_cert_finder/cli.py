from sys import exit as sys_exit
from signal import signal, SIGINT

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
    signal(SIGINT, ctrl_c_handler) # Handle Ctrl + C

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

    for problem in problematic_certs:
        print(problem)

    if settings.send_to_slack and len(problematic_certs) > 0:
        send_to_slack(problematic_certs)


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

    return problematic_certs

def ctrl_c_handler(sig, frame):
    sys_exit(0)

def run():
    Fire(cli_runner)