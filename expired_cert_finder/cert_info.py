from time import strftime, strptime, mktime, time
from re import sub

from expired_cert_finder.settings import Settings

from OpenSSL.crypto import load_certificate, FILETYPE_PEM, FILETYPE_ASN1, Error as Crypto_Error

def get_cert_information(certificate, raw=False):
    try:
        if not raw: # we only want to remove padding on whole certificates rather than bytes.
            certificate = sub(r"\n {0,}", "\n", certificate) # remove padding at begining of new lines.

        cert_type = FILETYPE_PEM if not raw else FILETYPE_ASN1

        parsed = load_certificate(cert_type, certificate)

        timestamp = strptime(parsed.get_notAfter().decode("utf-8"), '%Y%m%d%H%M%SZ')
        diff = mktime(timestamp) - time()

        not_after = strftime('%Y-%m-%d', timestamp)

        expiry_window = 60 * 60 * 24 * int(Settings.instance().expiry_window)

        close_to_expiry = diff < expiry_window and diff > 0

        return {
            'not_after': not_after,
            'is_expired': diff < 0,
            'close_to_expiry': close_to_expiry,
            'subject': parsed.get_subject().CN
        }
    except Crypto_Error as ex_ce:
        if ex_ce.args[0][0][2] == 'no start line':
            if not raw:
                return get_cert_information(certificate, True)
        # elif ex_ce.args[0][0][2] == 'wrong tag' and raw: # Switch from base64 encoded data to raw bytes.
        #     if type(certificate) is not bytes:
        #         return get_cert_information(b64decode(certificate), True)
        elif ex_ce.args[0][0][2] == 'not enough data': # Random data picked up as base64
            pass
        elif ex_ce.args[0][0][2] == 'header too long': # Not a certificate, usually encrypted password.
            pass
        else:
            raise


class CertInfo:
    def __init__(self, discovered_by, path, certificate):
        self.discovered_by = discovered_by
        self.path = path 
        self.certificate = certificate

    def getInfo(self):
        return get_cert_information(self.certificate)
