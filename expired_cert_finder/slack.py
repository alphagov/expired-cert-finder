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

def get_list_of_problematic_certs(expired, immediate_action, next_7_days, remaining):

    constructed_list = ""

    if len(expired) > 0:
        constructed_list += ":alert: The following certs have EXPIRED :alert:"
        for problem_cert in expired:
            constructed_list += CERTIFICATE_PAYLOAD_SECTION.substitute(certificate_name=problem_cert['message'])

    if len(immediate_action) > 0:
        constructed_list += ":alert: The following certs require IMMEDIATE ACTION :alert:"
        for problem_cert in immediate_action:
            constructed_list += CERTIFICATE_PAYLOAD_SECTION.substitute(certificate_name=problem_cert['message'])

    if len(next_7_days) > 0:
        constructed_list += ":warning: The following certs expire in the next 7 days :warning: "
        for problem_cert in next_7_days:
            constructed_list += CERTIFICATE_PAYLOAD_SECTION.substitute(certificate_name=problem_cert['message'])

    if len(remaining) > 0:
        constructed_list += ":information_source: The following certs expire in more than 7 days :information_source:"
        for problem_cert in remaining:
            constructed_list += CERTIFICATE_PAYLOAD_SECTION.substitute(certificate_name=problem_cert['message'])

    return \
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": constructed_list[:-1]
        }
    }


def send_to_slack(expired, immediate_action, next_7_days, remaining):
    settings = Settings.instance()

    client = WebhookClient(settings.slack_webhook_url)

    formatted_certs_block = get_list_of_problematic_certs(expired, immediate_action, next_7_days, remaining)

    blocks = BLOCKS
    blocks.append(formatted_certs_block)

    response = client.send(text=FALLBACK_TEXT, blocks=blocks)

    if response.status_code != 200:
        print("Failed to send to Slack.")

    if settings.debug:
        print(response)
