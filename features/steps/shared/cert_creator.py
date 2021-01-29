from os import system

def create_certs(days, pre_ramble=False):
    if type(days) == str:
        days = int(days)

    faketime = ""
    validity = days
    
    if days < 0:
        faketime = "faketime -f %dd " % days
        validity = -1 * days


    open_ssl_cmd = """
        openssl req -x509 -newkey rsa:2048 \
        -keyout work/key.pem \
        -out work/cert.pem \
        -nodes \
        -days %d \
        -subj \"/C=GB/ST=London/L=London/O=Cert Checker/OU=Certification/CN=Cert Checker\"
    """ % validity

    cmd = faketime + open_ssl_cmd.strip()

    if pre_ramble is True:
        cmd += " -text"

    # print(cmd)
    system(cmd)
