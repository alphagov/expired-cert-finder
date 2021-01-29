from base64 import b64encode

def read_cert_file():
    return ''.join(open('./work/cert.pem').readlines())

def get_base64_encoded_cert_string():
    return b64encode(read_cert_file().encode("utf-8")).decode("ascii")