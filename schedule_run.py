import subprocess
import schedule
import time
import datetime

from utils import check_if_weekday, is_trading_day


def job_print_time():
    print(datetime.datetime.now().time())


def job_scrape_fear_idx():
    if is_trading_day():
        script_path = ".\scrape_fear_idx.py"
        # Run the script using Python
        command = f"python {script_path}"
        print("run job: scrape_fearidex")
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("Not trading day, scrape fear idex skipped.")


def job_scrape_cme():
    if is_trading_day():
        script_path = ".\scrape_cme.py"
        # Run the script using Python
        command = f"python {script_path}"
        print("run job: scrape_cme")
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("Not trading day, scrape cme skipped.")


# schedule.every().day.at("08:00").do(check_if_weekday)
schedule.every().day.at("09:00").do(job_scrape_fear_idx)
schedule.every().day.at("18:00").do(job_scrape_cme)
schedule.every().hour.at(":01").do(job_print_time)
# schedule.every().minute.at(":01").do(job)

print('Schedule Started')

# Keep the script running indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)  # use 1 second

# prevent the console from closing
input('Press Enter to exit...')
