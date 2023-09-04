from _secret import LukeLab_Email, MY_EMAIL, RECEIVER_EMAILS
from utils import send_email, send_emails

email_msg_body_tmp = 'test email for tset'
send_email(LukeLab_Email, MY_EMAIL, 'FGI Scraper Notify: End1', email_msg_body_tmp)
send_emails(LukeLab_Email, RECEIVER_EMAILS, 'FGI Scraper Notify: End2', email_msg_body_tmp)