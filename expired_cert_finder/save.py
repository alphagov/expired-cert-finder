from expired_cert_finder.settings import Settings


def save_file(problematic_certs):
    settings = Settings.instance()
    expired_cert_list_filename = settings.expired_cert_list_filename

    with open(expired_cert_list_filename, "w") as f:
        for expired in problematic_certs:
            f.write(expired + '\n')

    if settings.ui:
        print("List of expired certificates written to %s" % expired_cert_list_filename)
    