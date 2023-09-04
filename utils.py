import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from _secret import LukeLab_Email, LukeLab_Email_Pwd


def send_email(from_, to, msg_subject, msg_body):
    # create message
    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = msg_subject

    # add text to message
    msg.attach(MIMEText(msg_body))

    # setup gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = LukeLab_Email
    smtp_password = LukeLab_Email_Pwd

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_emails(from_, to: list, msg_subject, msg_body):
    # send an email to multiple recipients

    sender_email = from_
    receiver_emails = to  # ['recipient1@example.com', 'recipient2@example.com']
    # message = msg_body
    #
    # msg = MIMEText(message)

    message = f"""<pre style="font-family: 'Courier New', monospace;">{msg_body}</pre>"""

    msg = MIMEText(message, 'html')  # change the font style with Equal-Width Characters

    msg['Subject'] = msg_subject
    msg['From'] = sender_email
    msg['To'] = LukeLab_Email
    # msg["Cc"] = ''
    # msg['Bcc'] = ', '.join(receiver_emails)
    # toaddrs = [msg['To']] + [msg['Bcc']]

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(LukeLab_Email, LukeLab_Email_Pwd)
        server.sendmail(LukeLab_Email, ['lukelabtorary@gmail.com'] + receiver_emails, msg.as_string())


def set_up_app_logging():
    # set up logging
    log_file = os.path.join(os.getcwd(), 'running.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def logging_info(message: str):
    set_up_app_logging()
    logging.info(f'>>> {message}')  # write log
