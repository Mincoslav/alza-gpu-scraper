import logging
import time
import datetime
from random import randrange
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from alza_gpu_scraper import send_email

url = 'https://eshop.ciernediery.sk/'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = selenium.webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(20)
mail = ''


def main():
    try:
        while True:
            driver.get(url)
            print(url)
            xpath = '//*[@id="nm-shop-browse-wrap"]/ul/li[1]/div[1]/a/span'
            style_to_check = 'background-image: url("https://d3i9l7sj72swdx.cloudfront.net/eshop-ciernediery-sk/Prelepka_VYPREDANE.png");'
            time.sleep(randrange(5, 10, 1))

            if driver.find_element_by_xpath(xpath).get_attribute("style") != style_to_check:
                current_time = datetime.datetime.now()
                # screenshot = driver.get_screenshot_as_png()
                logging.info('Sending email at {}'.format(current_time))
                send_email("{} at time: {}".format(url, current_time), "Update on {}".format(url), mail,
                           '', '')
                logging.info('Email sent at {}'.format(datetime.datetime.now()))
                logging.info("sleeping for {}".format(str(300)))
                time.sleep(300)
            else:
                timer = randrange(120, 300)
                logging.info("Current time: {}".format(str(datetime.datetime.now())))
                logging.info("sleeping for {}".format(str(timer)))
                time.sleep(timer)
                driver.refresh()
    except Exception as exception:
        current_time = datetime.datetime.now()
        send_email("Exception thrown: \n{}".format(exception),
                   "Cierne diery monitoring failed at time: {}".format(current_time), mail,
                   '', '')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
