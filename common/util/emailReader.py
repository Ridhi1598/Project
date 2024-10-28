import datetime
import imaplib
import traceback
import email
from datetime import datetime


from future.backports.datetime import timedelta


def validate_last_email(context, emailId, password, sender, subject):
    ORG_EMAIL = "@gmail.com"
    FROM_EMAIL = emailId + ORG_EMAIL
    FROM_PWD = password
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993

    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['date']
                    dateSet = email_date.rpartition(' ')
                    print(dateSet[0])
                    date_time_obj = datetime.strptime(dateSet[0], '%a, %d %b %Y %H:%M:%S')
                    now = datetime.utcnow()
                    dt_string = now.strftime("%a, %d %b %Y %H:%M:%S")
                    my_date_time_obj = datetime.strptime(dt_string, '%a, %d %b %Y %H:%M:%S')
                    new_final_time = my_date_time_obj + timedelta(minutes=2)
                    if new_final_time >= date_time_obj:
                        if email_from == sender and email_subject == subject:
                            return "success"
                        else:
                            return "fail"
                    break
            break
    except Exception as e:
        traceback.print_exc()
        print(str(e))
