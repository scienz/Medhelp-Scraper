'''
This module fetches the link to each post in the scroll-able pages
in the frontier.

The return value is a generator rather than a frontier (list) is mainly
for memory-management purposes.

The links fetched by this module should be passed to post_scraper.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_post_link(url, driver_path = None):
    script = _get_script()
    driver = _config_driver(url, driver_path)

    pageLen = driver.execute_script(script)
    while (True):
        lastLen = pageLen
        time.sleep(1)
        pageLen = driver.execute_script(script)
        if lastLen == pageLen:
            break

        for e in driver.find_elements_by_xpath('//div[@class="subj_stats"]//a'):
            link = e.get_attribute("href")
            yield link
    driver.quit()

def get_scrolled_page(url, driver_path = "F:\\ChromeDriver\\chromedriver.exe"):
    script = _get_script()
    driver = _config_driver(url, driver_path)

    pageLen = driver.execute_script(script)
    while (True):
        lastLen = pageLen
        time.sleep(4)
        pageLen = driver.execute_script(script)
        if lastLen == pageLen:
            break

    page = driver.page_source.encode('utf-8')
    driver.quit()
    return page

# url: lnks the scroll-able page returned from the frontier
# driver_path: the path to the chrome driver
def _config_driver(url, driver_path = "F:\\ChromeDriver\\chromedriver.exe"):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path= driver_path,
        options= options)
    driver.get(url)
    return driver

def _get_script():
    script = ("window.scrollTo(0, document.body.scrollHeight);"
                "return document.body.scrollHeight;")
    return script
