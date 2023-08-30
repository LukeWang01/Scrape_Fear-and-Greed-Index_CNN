import scrapy
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path="C:\LukeLab\Web-Development\crafting\chromedriver.exe")

driver.get("https://www.cnn.com/markets/fear-and-greed")
time.sleep(10)

time_idex_dict = {}

for i in range(100):
    time_em = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__timestamp')
    # time.click()

    timestamp = time_em.get_attribute("data-timestamp")
    idex = driver.find_element(By.CLASS_NAME, 'market-fng-gauge__dial-number-value')

    print(time_em.text)
    # print(type(time.text))
    print(timestamp)
    # print(type(timestamp))
    print(idex.text)
    # print(type(idex.text))
    print('-----------------')
    time_idex_dict[timestamp] = int(idex.text)
    time.sleep(120)

time.sleep(10)
driver.close()
time.sleep(10)
driver.quit()


# input.send_keys("Python")
# time.send_keys(Keys.ENTER)

# form = driver.find_element(By.CLASS_NAME, 'form-control')
#
# form.send_keys("myname",Keys.TAB,"mylastname", Keys.TAB, "myemailadress@gmail.com", Keys.TAB,Keys.ENTER)

# In Selenium, each window has a identification handle, we can get all the window handles with:
# driver.window_handles

# from selenium.common.exceptions import NoSuchElementException

class Test(scrapy.Spider):
    name = 'Test'
    url = "https://books.toscrape.com/"

    def parse(self, response):
        for article in response.css('article.product_pod'):
            yield {
                'price': article.css(".price_color::text").extract_first(),
                'title': article.css("h3 > a::attr(title)").extract_first()
            }


#

class IndexSpider(scrapy.Spider):
    name = 'IndexSpider'
    url = "https://www.cnn.com/markets/fear-and-greed"

    def parse(self, reponse):
        for line in reponse.css('div.market-fng-indicator'):
            yield {
                'index value': line.css('.market-fng-indicator__name::text').extract_first()
            }
