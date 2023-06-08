import logging
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sqlite3

import time
import datetime
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from _secret import LukeLab_Email_Pwd, LukeLab_Email

# import chromedriver_autoinstaller as chromedriver
# chromedriver.install()
# driver update: https://chromedriver.chromium.org/downloads

""" # 1. Global variables:  """
MY_EMAIL = 'wangzilu9488@gmail.com'
DRIVER_PATH = "chromedriver.exe"
TARGET_URL = "https://www.cnn.com/markets/fear-and-greed"

# add more receivers here:
RECEIVER_EMAILS = ['wangzilu9488@gmail.com', 'road_prince@outlook.com']

""" # 2. Utils functions: """


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
    message = msg_body

    msg = MIMEText(message)
    msg['Subject'] = msg_subject
    msg['From'] = sender_email
    msg['To'] = 'wangzilu9488@gmail.com'
    # msg["Cc"] = ''
    # msg['Bcc'] = ', '.join(receiver_emails)
    # toaddrs = [msg['To']] + [msg['Bcc']]

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(LukeLab_Email, LukeLab_Email_Pwd)
        server.sendmail(LukeLab_Email, ['wangzilu9488@gmail.com'] + receiver_emails, msg.as_string())


# Set up app running log
def set_up_app_logging():
    # set up logging
    log_file = os.path.join(os.getcwd(), 'running.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def logging_info(message: str):
    set_up_app_logging()
    logging.info(f'>>> {message}')  # write log


def save_data(time_index_list, table_name):
    # time_index_list: list of tuple, (timestamp:int, date_time:str, idx:int)

    # connect to the table
    conn = sqlite3.connect("FearAndGreedyIndex.db")
    c = conn.cursor()

    # get all tables in the FearAndGreedyIndex.db
    c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    table_list = c.fetchall()

    # if table doesn't exist, create the table
    if table_name not in [i[0] for i in table_list]:
        c.execute(f"CREATE TABLE {table_name} (time_stamp INTEGER, date_time TEXT, idx_data INTEGER);")
        # c.execute("CREATE TABLE index_data (time_stamp INTEGER, date_time TEXT, idx_data INTEGER);")
        # c.execute("CREATE TABLE friends (first_name TEXT, last_name TEXT, closeness INTEGER);")
        conn.commit()
        # conn.close()
        print('database and table created...')
    else:
        print('database and table already created...')

    c.executemany(f"INSERT INTO {table_name} VALUES (?,?,?);", time_index_list)
    conn.commit()
    conn.close()
    print('data saved...')
    print('--------->')


# def close_db():
#     conn = sqlite3.connect("FearAndGreedyIndex.db")
#     conn.close()


""" # 3. Scrape functions: """


def get_time_index_list(hours=8, table_name='index_data'):
    # hours (int): input the hours duration to run
    # table_name (str): input the database table to save to

    """
    The executable_path parameter in webdriver.Chrome is deprecated in newer versions of Selenium.
    Instead, you can pass a Service object as the service parameter.

    # driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    """
    start_email_sent = False

    # Create a Service object
    service = Service(DRIVER_PATH)

    # Create a WebDriver instance
    try:
        driver = webdriver.Chrome(service=service)
    except:
        print("Please update driver")
        send_email(LukeLab_Email, MY_EMAIL, 'FGI Scraper Notify: driver update', 'Please update the driver')
        return

    driver.maximize_window()
    driver.get(TARGET_URL)
    time.sleep(5)  # wait webpage loading
    print('web drive launched...')
    time.sleep(1)
    print('--------->')

    minutes = hours * 60
    time_index_list_tmp = []
    time_index_list = []

    time.sleep(60)  # wait the page to fully loaded

    # driver.minimize_window()  # minimize the browser window to save the memory

    for i in range(minutes):

        try:
            # get the timestamp from the webpage
            time_em = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__timestamp')
            timestamp = time_em.get_attribute("data-timestamp")
            if len(timestamp) == 0:
                timestamp = 0

            # get the index value from the webpage
            index = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__dial-number-value')
            if len(index.text) == 0:
                index.text = 0

            # get the current datetime from system
            current_date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            # combine the data as tuple and append to list
            time_index = (int(timestamp), current_date_time, int(index.text))
            time_index_list_tmp.append(time_index)
            logging_info(f'>>> {time_index}')

            # save the index data every 10 minutes
            if (i % 10 == 0) and (i > 0):
                table_name_tmp = table_name + '_' + datetime.datetime.now().strftime("%d_%m_%Y")
                save_data(time_index_list_tmp, table_name_tmp)
                save_data(time_index_list_tmp, table_name)
                time_index_list_tmp = []  # empty the list to avoid duplicate data

            print(time_index)  # print current index for log
            time_index_list.append(time_index)

            # send email when the scraper starts, with initial index value
            if not start_email_sent:
                send_email(LukeLab_Email, MY_EMAIL, 'FGI Scraper Notify: Start',
                           'FGI Scraper Started, from Road device')

                schedule_msg_body = f"FGI Scraper Started, \n" \
                                    f"Time: 09:50 AM EST, good morning / evening, \n" \
                                    f"Fear & Greed Index: {time_index[2]} \n" \
                                    f"A Fear & Greed Index daily summary will be sent after the market closed.\n"

                schedule.every().day.at("09:50").do(send_emails, LukeLab_Email, RECEIVER_EMAILS,
                                                    'FGI Scraper Notify: Start', schedule_msg_body)

                start_email_sent = True

            schedule.run_pending()

            time.sleep(60)  # wait every 60 sec

        except:
            print("An exception occurred, skip to next run in 5 minutes.")
            driver.refresh()
            time.sleep(300)
            print("Page refreshed")
            continue

    # for loop end and scrape completed
    print('Scrape Completed')
    # print(time_index_list)
    # save_data(time_index_list, table_name)

    # quit the scrape and web drive
    time.sleep(2)
    driver.close()
    time.sleep(5)
    driver.quit()
    print('web drive terminated')

    # send email when the scraper ends
    morning_index = time_index_list[0][2]
    noon_index = time_index_list[int(len(time_index_list) // 2)][2]
    afternoon_index = time_index_list[-1][2]
    all_index = [i[2] for i in time_index_list]
    end_msg = f"FGI Scraper Ended, from Road device, {len(time_index_list)} data points scraped. \n " \
              f"Morning Index: {morning_index} \n " \
              f"Noon Index: {noon_index} \n " \
              f"Afternoon Index: {afternoon_index}" \
              f"Max index: {max(all_index)} \n" \
              f"Min index: {min(all_index)} \n"

    send_emails(LukeLab_Email, RECEIVER_EMAILS, 'FGI Scraper Notify: End', end_msg)


# start, run only once to creat the database:
# creat_db("FearAndGreedyIndex.db")
# Call the scrape function to run
# Input: hours, table name to save
# Check if it's a workday (Monday to Friday)

""" # 4. Run: """
today = datetime.datetime.now().date()
if today.weekday() < 5:
    get_time_index_list(8, "index_data")
else:
    print("Today is not a workday, skip the scrape.")

# prevent the console from closing
input('Press Enter to exit...')
