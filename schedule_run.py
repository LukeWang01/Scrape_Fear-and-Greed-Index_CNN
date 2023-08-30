import subprocess
import schedule
import time
import datetime


def job():
    if check_if_weekday():
        # Replace with the path to your Python script
        script_path = ".\scrape_fear_idex.py"
        # Run the script using Python
        command = f"python {script_path}"
        # subprocess.call(command, shell=True)
        print("run job: scrape_fearidex")
        # Execute command in a new console window
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("scrape_fearidex skipped.")


# Schedule the job to run every workday (Monday to Friday) at 9:00 am EST
# schedule.every().monday.to.friday.at("9:00").do(job)
# Define the start and end time
# start_time = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
# end_time = start_time + datetime.timedelta(minutes=20)
# Schedule the job every weekday between the start and end time
# schedule.every().weekday().during(start_time.time(), end_time.time()).do(job)

def print_time():
    print(datetime.datetime.now().time())


def check_if_weekday():
    tmp = datetime.datetime.now().date()
    if tmp.weekday() < 5:
        print("Today is a workday, starting the scrape at 9:00 am.")
        return True
    else:
        print("Today is not a workday, skip the scrape.")
        return False


# schedule.every().day.at("08:00").do(check_if_weekday)
schedule.every().day.at("09:00").do(job)
schedule.every().hour.at(":01").do(print_time)

print('Schedule Started')

# Keep the script running indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)   # change to 5 seconds, reduce the cpu usage
    # use 1 second
