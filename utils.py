import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas_market_calendars as mcal
from datetime import datetime


import yfinance as yf
from datetime import datetime

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
    # ['recipient1@example.com', 'recipient2@example.com']
    receiver_emails = to
    # message = msg_body
    #
    # msg = MIMEText(message)

    message = f"""<pre style="font-family: 'Courier New', monospace;">{
        msg_body}</pre>"""

    # change the font style with Equal-Width Characters
    msg = MIMEText(message, 'html')

    msg['Subject'] = msg_subject
    msg['From'] = sender_email
    msg['To'] = LukeLab_Email
    # msg["Cc"] = ''
    # msg['Bcc'] = ', '.join(receiver_emails)
    # toaddrs = [msg['To']] + [msg['Bcc']]

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(LukeLab_Email, LukeLab_Email_Pwd)
        server.sendmail(
            LukeLab_Email, ['lukelabtorary@gmail.com'] + receiver_emails, msg.as_string())


def set_up_app_logging():
    # set up logging
    log_file = os.path.join(os.getcwd(), 'running.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def logging_info(message: str):
    set_up_app_logging()
    logging.info(f'>>> {message}')  # write log


def is_trading_day():
    # Get today's date
    today = datetime.now().date()

    # Specify the market calendar (e.g., 'XNYS' for New York Stock Exchange)
    nyse = mcal.get_calendar('XNYS')

    # Check if today is a valid trading day
    # return yes if today is a trading day, no if not.
    return nyse.valid_days(start_date=today, end_date=today).size > 0


def check_if_weekday():
    tmp = datetime.now().date()
    if tmp.weekday() < 5:
        print("Today is a workday, starting the scrape at 9:00 am.")
        return True
    else:
        print("Today is not a workday, skip the scrape.")
        return False
