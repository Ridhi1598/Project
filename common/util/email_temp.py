import logging
import time
# from exporter import EmailClient, EmailClientException

# Posting to a Slack channel
def send_message_to_slack(text):
    from urllib import request, parse
    import json

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))


logger = logging.getLogger('tornado.general')


def send_activation_email(self, **kwargs):
    title = 'Registration confirmation'
    content = '''The following user is interested in BI Portal:\n'''
    for k, v in kwargs.items():
        content += '{}: {}\n'.format(k, v)
    content += '''\n'''
    content += 'Visit user management page on BI-Portal to add user at {0}'.format(self.callback_url)
    admin_email_list = str(self.admin_email_list).split(',')
    self.logger.info("admin email lists")
    self.logger.info(admin_email_list)
    result = send_email(self, title, content, admin_email_list)
    if result:
        self.logger.info('Successfully sent to admins.')
        return "success"
    else:
        self.logger.error('Failed to notify the admins!!!')
        return "error"


def send_contact_support_email(self, body, **kwargs):
    title = body.get("subject")
    content = '''********** THIS IS SYSTEM GENERATED MAIL PLEASE DONOT REPLY **********\n'''
    content += '''\n'''
    for k, v in kwargs.items():
        content += '{}:  {}\n'.format(k, v)
    content += '''\n'''
    content += body.get("message")
    admin_email_list = [body.get("to_email")]
    result = send_email(self, title, content, admin_email_list)
    if result:
        self.logger.info('Successfully sent to admins.')
        return "success"
    else:
        self.logger.error('Failed to notify the admins!!!')
        return "error"


def send_email(title, content, recipients, attachment, exporter_server_host, exporter_server_port):
    if not recipients or type(recipients) not in [list, str]:
        return False
    elif isinstance(recipients, str):
        recipients = [recipients]
    try:
        exporter_info = {
            'address': exporter_server_host,
            'port': int(exporter_server_port)
        }
        email_client = EmailClient(**exporter_info)

    except Exception as e:
        logger.error(e)
        return False
    logger.info(recipients)
    for recipient in recipients:
        try:
            pkt_id, status = email_client.send(recipient, title, content, attachment_path=attachment, reconnect=True)
            logger.info('{}, {}'.format(pkt_id, status))
            for i in range(2):
                result = email_client.check_output(pkt_id)
                if result is not None:
                    logger.info('response from exporter client: {}'.format(result))
                    break
                else:
                    time.sleep(5)

            if status < 0:
                raise EmailClientException

        except Exception as e:
            logger.error(e)
            return False
        finally:
            email_client.close()
    return True
