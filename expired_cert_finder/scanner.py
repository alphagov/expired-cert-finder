#! /usr/bin/env python

from expired_cert_finder.plugins.raw import RawParser
from expired_cert_finder.plugins.yaml import YamlParser

from expired_cert_finder.allowed_certs import AllowedCerts

rawParser = RawParser
yamlParser = YamlParser

# handle dynamic loading.

def scan_file_for_certificate(path, expired_only, debug):
    results = []
    try:
        if path in AllowedCerts.instance().allowed_certs:
            return results

        file = open(path, "r")
        file_contents = file.read()

        run_default = True

        certs = []
        if path.endswith('.yaml') or path.endswith('.yml'):
            try:
                certs = yamlParser.process(path, file_contents, debug)
                run_default = False
            except Exception as ex:
                if debug:
                    print("Error while using YAML Parser: " + path)
                    print(ex)
                pass

        if run_default:
            certs = rawParser.process(path, file_contents, debug)

        for cert in certs:
            try:
                cert_info = cert.getInfo()
                if cert_info is not None and (cert_info['is_expired']
                or (cert_info['close_to_expiry'] and expired_only == False)):
                    status = "EXPIRED" if cert_info['is_expired'] else "CLOSE_TO_EXPIRY"
                    results.append('%s, %s, %s: %s' % (cert.path, cert_info['subject'], status, cert_info['not_after']))
            except Exception as e:
                print(cert, e)
                raise

    except UnicodeDecodeError:
        pass
    except Exception as ex:
        if debug:
            print("File that caused exception: %s" % path)
            raise ex
        else:
            print("Error processing %s, %s" % (path, ex))

    return results
