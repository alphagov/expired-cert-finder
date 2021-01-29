from re import finditer
from expired_cert_finder.plugins.helpers.plugin import Plugin

from expired_cert_finder.cert_info import CertInfo
from expired_cert_finder.regexs import FIND_CERT_REGEX

def find_raw_certs(path, file_contents):
    certs = finditer(FIND_CERT_REGEX, file_contents)

    certs_to_process = []
    for m in certs:
        line_number = find_line_number(m.start(), file_contents)
        path_with_line_number = '%s:%s' % (path, line_number)

        certs_to_process.append(CertInfo("raw", path_with_line_number, m.group(0)))

    return certs_to_process

def find_line_number(cert_start, file_content):
    before_cert = file_content[:cert_start+1] # plus 1 as we strip the new line in the regex.

    return before_cert.count('\n') + 1 # plus one as we start at line 1 not line 0.

class RawParser(Plugin):
    def process(path, file_contents, debug=False):
        return find_raw_certs(path, file_contents)

    def getType():
        return ['.*']