FIND_CERT_REGEX = r"(?:\s{0,})?(-{5}BEGIN CERTIFICATE-{5}\n[\s\w\d\n\/\+]{0,}={0,3}\n(?:\s{0,})-{5}END CERTIFICATE-{5})"
FIND_BASE64_REGEX = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$"
