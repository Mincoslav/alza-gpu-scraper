import time
from tkinter import messagebox

import selenium.webdriver
import yagmail
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = selenium.webdriver.Chrome(options=chrome_options)


def send_email(contents: str, subject: str, receiver: str, user: str, password: str):

    yag = yagmail.SMTP(user, password)
    yag.send(
        to=receiver,
        subject=subject,
        contents=contents,
    )


def main():
    while True:
        driver.get('https://www.alza.sk/graficke-karty-nvidia-geforce-rtx-3060-ti/18884150.htm')
        xpath = '//*[@data-impression-category="Komponenty \ Grafické karty \ NVIDIA"]'
        main_page = EC.visibility_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, 20).until(main_page)

        cards = driver.find_elements_by_xpath(xpath)
        del cards[::2]

        for card in cards:

            if "Na sklade" in card.get_attribute('data-impression-dimension13'):
                messagebox.showinfo("Na sklade", '\n-------------------------------'
                                    + card.get_attribute('data-impression-name')
                                    + "\n" + card.get_attribute('href') + "\n"
                                    + card.get_attribute('data-impression-dimension13') + '✔')

                send_email("Na sklade" + '\n-------------------------------'
                           + card.get_attribute('data-impression-name')
                           + "\n" + card.get_attribute('href') + "\n"
                           + card.get_attribute('data-impression-dimension13') + '✔',
                           "Wake the fuck up Samurai, there's a GPU to scalp")

            elif "Očakávame" in card.get_attribute('data-impression-dimension13'):
                print(card.get_attribute('data-impression-name') + " -> "
                      + card.get_attribute('data-impression-dimension13') + " ❔")

            else:
                print(card.get_attribute('data-impression-name') + " -> "
                      + card.get_attribute('data-impression-dimension13') + " ❌")

        time.sleep(5)
        driver.refresh()


if __name__ == '__main__':
    main()