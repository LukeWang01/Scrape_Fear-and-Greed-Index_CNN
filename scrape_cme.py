from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from _secret import LukeLab_Email, RECEIVER_EMAILS, discord_channel_cme_fed_watch_tool_id
from send_discord_msg_web_auth import send_msg_to_discord_request
from utils import send_emails


def get_meeting_pro_and_total_prob():
    # Specify the URL
    url = "https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html?redirect=/trading/interest-rates/countdown-to-fomc.html"
    DRIVER_PATH = "chromedriver.exe"

    service = Service(DRIVER_PATH)

    # Create a WebDriver instance
    driver = webdriver.Chrome(service=service)

    # Open the URL
    driver.maximize_window()
    driver.get(url)
    title = driver.title
    # print(title)

    # Wait for the data to load (adjust the sleep time as needed)
    time.sleep(5)

    # Find the data elements using their XPath
    iframe = driver.find_element(By.ID, 'cmeIframe-jtxelq2f')
    # print(iframe)
    # driver.execute_script("arguments[0].scrollIntoView();", iframe)
    scroll_distance = 800
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    time.sleep(1)

    driver.switch_to.frame(iframe)
    prob = driver.find_element(By.ID, 'ctl00_MainContent_ucViewControl_IntegratedFedWatchTool_lbPTree')
    # print(prob)
    prob.click()
    time.sleep(10)

    # total_probabilities = driver.find_element(By.XPATH, '//*[@id="MainContent_pnlContainer"]/div[3]/div/div/table[3]/tbody')
    # grid-thm grid-thm-v2
    # update the xpath
    # //*[@id="MainContent_pnlContainer"]/div[3]/div/div/div[2]/table/tbody
    total_probabilities = driver.find_element(By.XPATH, '//*[@id="MainContent_pnlContainer"]/div[3]/div/div/div[2]/table/tbody')
    # print(total_probabilities)
    rows = total_probabilities.find_elements(By.TAG_NAME, 'tr')

    prob_res = ''
    head = 'MEETING_DATE,DAYS_TO_MEETING,Ease,No_Change,Hike'

    for row in rows:
        line = ''
        try:
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                line += cell.text + ','
            line = line[:-1]
            prob_res += line + '\n'
        except:
            continue

    prob_res = head + '\n' + prob_res
    # print(prob_res)

    lines = prob_res.strip().split('\n')
    header = lines[0]
    data_lines = lines[3:]  # Exclude the empty line and header

    formatted_header = "{:<14} {:<15} {:<8} {:<10} {:<8}".format(*header.split(','))
    formatted_lines = []

    for line in data_lines:
        parts = line.split(',')
        formatted_line = "{:<14} {:<15} {:<8} {:<10} {:<8}".format(*parts)
        formatted_lines.append(formatted_line)

    total_probabilities_res = formatted_header + '\n'
    for line in formatted_lines:
        total_probabilities_res += line + '\n'

    total_probabilities_res = 'Total Probabilities:' + '\n' + total_probabilities_res

    # meeting probabilities
    # grid-thm grid-thm-v2
    # update the xpath
    # meeting_probabilities = driver.find_element(By.XPATH, '//*[@id="MainContent_pnlContainer"]/div[3]/div/div/table[2]/tbody')
    meeting_probabilities = driver.find_element(By.XPATH, '//*[@id="MainContent_pnlContainer"]/div[3]/div/div/div[1]/table/tbody')
    meeting_probabilities_rows = meeting_probabilities.find_elements(By.TAG_NAME, 'tr')

    tmp = ''
    for i in range(len(meeting_probabilities_rows)):
        line = ''
        highlight = ['-1']
        if i == 0:
            continue
        if i == 1:
            cells = meeting_probabilities_rows[i].find_elements(By.TAG_NAME, 'th')
        else:
            cells = meeting_probabilities_rows[i].find_elements(By.TAG_NAME, 'td')
            highlight = meeting_probabilities_rows[i].find_elements(By.CLASS_NAME, 'number.highlight2')
            # print(highlight[0].text)
        for cell in cells:
            txt = cell.text
            try:
                highlight_txt = highlight[0].text
            except:
                highlight_txt = '-1'
            if highlight_txt == txt:
                txt = '<' + txt + '>'
            line += txt + ','
        line = line[:-1]
        tmp += line + '\n'

    lines = tmp.strip().split("\n")

    # Find the maximum width for each column
    column_widths = [15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    # Reformat the data with aligned columns
    formatted_data = ""
    for line in lines:
        cells = line.split(",")
        formatted_line = ""
        for i, cell in enumerate(cells):
            formatted_line += cell.ljust(column_widths[i])
        formatted_data += formatted_line.rstrip(",") + "\n"

    meeting_probabilities_res = 'Meeting Probabilities:' + '\n' + formatted_data

    # Close the webdriver
    print('Scraping completed... quitting the driver in 10s')
    time.sleep(10)
    driver.quit()

    return meeting_probabilities_res, total_probabilities_res


if __name__ == '__main__':
    try:
        meeting_probabilities_res, total_probabilities_res = get_meeting_pro_and_total_prob()
        print(meeting_probabilities_res)
        print(total_probabilities_res)
        end_msg = ""
        end_msg += "```\n"
        end_msg += meeting_probabilities_res + '\n'
        end_msg += total_probabilities_res + '\n'
        end_msg += "```\n"
    except Exception as e:
        print('scrape error, please check the element path...')
        print(e)
        end_msg = 'error from chrome driver, please check the HTML element path...'

    try:
        # send_emails(LukeLab_Email, RECEIVER_EMAILS, 'FGI Scraper Notify', end_msg)
        # time.sleep(3)
        send_msg_to_discord_request(end_msg, channel_id=discord_channel_cme_fed_watch_tool_id)
    except Exception as e:
        print('send emails CME error...')
        print(e)
        time.sleep(3)

    input('Press Enter to exit...')
