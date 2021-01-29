from expired_cert_finder.settings import Settings

from string import Template

from slack_sdk.webhook import WebhookClient

FALLBACK_TEXT = "Problematic certificates found!"

BLOCKS =  [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Problematic certificates found!"
        }
    },
    {
        "type": "divider"
    }
]

CERTIFICATE_PAYLOAD_SECTION = Template("* $certificate_name\n")

def get_list_of_problematic_certs(problematic_certs):

    constructed_list = ""

    for problem_cert in problematic_certs:
        constructed_list += CERTIFICATE_PAYLOAD_SECTION.substitute(certificate_name=problem_cert)

    return \
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": constructed_list[:-1]
        }
    }


def send_to_slack(problematic_certs):
    settings = Settings.instance()

    client = WebhookClient(settings.slack_webhook_url)

    formatted_certs_block = get_list_of_problematic_certs(problematic_certs)

    blocks = BLOCKS
    blocks.append(formatted_certs_block)

    response = client.send(text=FALLBACK_TEXT, blocks=blocks)

    if response.status_code != 200:
        print("Failed to send to Slack.")

    if settings.debug:
        print(response)