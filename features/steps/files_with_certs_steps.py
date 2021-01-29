from os import walk
from subprocess import run

from features.steps.shared.cert_creator import create_certs

@given(u'a file exists with a certificate with expiry of "{days}" days')
def create_cert_files(context, days):
    create_certs(days)


@when(u'certificate checker is run')
def run_cert_checker(context):
    cert_check_process = run("python . --ui=False --allowed-list=./work/expired_certificate_allowlist.config ./work", shell=True, capture_output=True)

    context.output = cert_check_process.stdout.decode('utf-8').splitlines()

    print(context.output)

    if cert_check_process.stderr:
        print(cert_check_process.stderr)

    assert cert_check_process.returncode == 0

@then(u'no expired certificates should be found')
def check_no_certs_found(context):
    if len(context.output) is not 0:
        print(context.output)

    assert len(context.output) is 0

@then(u'"{no_certs}" expired certificates should be found')
def x_expired_certs_found(context, no_certs):
    assert len(context.output) == int(no_certs)
    assert "EXPIRED" in context.output[0]

@then(u'"{no_certs}" expiring certificates should be found')
def x_expiring_certs_found(context, no_certs):
    assert len(context.output) == int(no_certs)
    assert "CLOSE_TO_EXPIRY" in context.output[0]

@when(u'files exist in directory')
def files_exist(context):
    _, _, files = next(walk("./work"))

    remove_from_list(files, 'expired_certificate_allowlist.config')

    assert len(files) > 0


def remove_from_list(list_obj, element):
    if element in list_obj:
        list_obj.remove(element)