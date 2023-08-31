### This is a tool to scrape the CNN Fear & Greedy Index, using selenium.

<br>

- Intall the required package: `pip install selenium` `pip install schedule`
- `sqlite3` is a built-in database in Python, just import.
- Double click `auto_run_scrape_fear_idex.bat` to run `scrape_fear_idex.py`
- To update the driver, goto: https://chromedriver.chromium.org/downloads
- Create a `_secret.py` file to save your email user name and password to send email out.


<br>

#### OR, run as schedule task on the cloud server:
- `python schedule_runn.py`, this cmd will schedule a task run every weekday at 9:00 am EST
- auto_schedule_run.bat file will auto run the cmd above.

<br>

#### There will be summary emails sending out every trading day after the market closed.

<br>

#### Examples:
![image1](img1.png "img1")
![image2](img2.png "img2")
![image](https://github.com/LukeWang01/Scrape_Fear-and-Greed-Index_CNN/assets/25569658/c564914c-4e9c-448f-84dc-c9960832cd8c)
![image](https://github.com/LukeWang01/Scrape_Fear-and-Greed-Index_CNN/assets/25569658/43a7aaa0-e5ec-42f3-b44f-fabb0487b5f2)

