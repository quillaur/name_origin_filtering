from selenium import webdriver
from selenium.common import exceptions
import time


def next_is_available()->bool:
    try: 
        driver.find_element_by_class_name("disabled next ")
    except exceptions.NoSuchElementException as e:
        return True

    return False


if __name__ == '__main__':
    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("https://www.pagesjaunes.fr/pagesblanches")

    driver.find_element_by_id("didomi-notice-agree-button").click()
    driver.find_element_by_id("ou").send_keys("Seine-Maritime (76)")
    driver.find_element_by_id("quoiqui").send_keys("MIN")
    driver.find_element_by_xpath("//button[@title='Trouver']").click()

    time.sleep(1)

    all_names = {}
    while True:
        all_names.extend([t.text for t in driver.find_elements_by_xpath("//li/div/header/div[1]/div/h3/a")])
        print(len(all_names))
        print(all_names[:15])

        if next_is_available():
            driver.find_element_by_xpath("//*[@id='pagination-next']").click()
            time.sleep(1)
        else:
            break