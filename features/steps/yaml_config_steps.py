from features.steps.shared.cert_creator import create_certs
from features.steps.shared.cert_reader import read_cert_file, get_base64_encoded_cert_string

from os import remove
from shutil import copy2


def remove_cert_files():
    remove('./work/key.pem')
    remove('./work/cert.pem')

def tab_each_line(text, number_of_tabs=1):
    prefix = ''
    output = ""

    # Tabs as spaces...
    for i in range(0, number_of_tabs):
        prefix += '    '

    for line in text.split('\n'):
        amended_line = prefix + line + '\n'
        output += amended_line

    return output


@given(u'a yaml file exists with a certificate with expiry of "{days}" days')
def create_yaml_with_cert(context, days):
    copy2('mocks/yaml_mock.yml', 'work/test.yml')

    create_certs(days, True)

    padded_cert =  tab_each_line(read_cert_file())

    writer = open("./work/test.yml", "a")
    writer.write(padded_cert)
    writer.close()


@given(u'a encoded yaml file exists with a certificate with expiry of "{days}" days')
def create_yaml_with_encoded_cert(context, days):
    copy2('mocks/yaml_encoded_mock.yml', 'work/test.yml')

    create_certs(days)

    encoded_cert = get_base64_encoded_cert_string()
    prepended = '  - ' + encoded_cert

    writer = open("./work/test.yml", "a")
    writer.write(prepended)
    writer.close()
    

@given(u'source cert material is removed')
def remove_source_material(context):
    remove_cert_files() 
