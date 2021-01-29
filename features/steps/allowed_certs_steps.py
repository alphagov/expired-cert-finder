from features.steps.shared.cert_reader import get_base64_encoded_cert_string

from os import path

@given(u'no allowed list in directory')
def check_if_allow_list_exists(context):
    assert path.isfile("./work/expired_certificate_allowlist.config") == False


@given(u'certificate path is added to allowed list')
def create_allowed_list_with_path_of_cert(context):
    writer = open("./work/expired_certificate_allowlist.config", "w")
    writer.write("./work/cert.pem\n")
    writer.close()


@given(u'certificates base64 encoded string is added to allowed list')
def step_impl(context):

    writer = open("./work/expired_certificate_allowlist.config", "w")
    writer.write(get_base64_encoded_cert_string())
    writer.close()

