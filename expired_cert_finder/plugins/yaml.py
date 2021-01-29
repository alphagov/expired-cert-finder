from re import search
from base64 import b64decode
from expired_cert_finder.allowed_certs import AllowedCerts
from expired_cert_finder.plugins.helpers.plugin import Plugin

from expired_cert_finder.cert_info import CertInfo
from expired_cert_finder.regexs import FIND_BASE64_REGEX, FIND_CERT_REGEX

from yaml import load_all, FullLoader
from yaml.parser import ParserError
from yaml.scanner import ScannerError
from yaml.constructor import ConstructorError

DEBUG = False

def find_certs_in_yaml(path, file_content):
    results = []
    yaml_docs = load_all(file_content, Loader=FullLoader)

    if type(yaml_docs) is dict:
        find_certs_in_yaml_nodes(results, yaml_docs)
    elif yaml_docs is not None:
        for yaml_doc in yaml_docs:
            find_certs_in_yaml_nodes(results, yaml_doc)

    certs_to_process = []
    for result in results:
        certs_to_process.append(CertInfo("yaml", path, result))

    return certs_to_process


def find_certs_in_yaml_nodes(captured_array, node):
    if node is None:
        return

    if isinstance(node, list):
        for element in node:
            find_certs_in_yaml_nodes(captured_array, element)
    elif isinstance(node, dict):
        for key, value in node.items():
            find_certs_in_yaml_nodes(captured_array, value)
    elif isinstance(node, str):
        handle_string_node_yaml(captured_array, node)


def handle_string_node_yaml(captured_array, node):
    input_str = node

    if input_str in AllowedCerts.instance().allowed_certs:
        return

    if search(FIND_BASE64_REGEX, input_str):
        input_str = b64decode(input_str).decode('utf-8')
        
    if search(FIND_CERT_REGEX, input_str):
        if DEBUG:
            print(input_str)
        captured_array.append(input_str)


class YamlParser(Plugin):
    def process(path, file_contents, debug=False):
        DEBUG = debug
        try:
            return find_certs_in_yaml(path, file_contents)
        except (ParserError, ScannerError, ConstructorError):
            raise

    def getType():
        return ['*.yaml', '*.yml']