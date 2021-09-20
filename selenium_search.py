"""
Usage: 
    selenium_search.py  [-hl NAME]

Options:
    -h --help    show this-
    -l --lastname NAME to search for [default: ""]
"""


from selenium import webdriver
from selenium.common import exceptions
import time
from docopt import docopt


if __name__ == '__main__':
    ###################
    #### Arguments ####
    ###################
    args = docopt(__doc__)

    lastname = args["--lastname"].lower()
    print(f"Searching for {lastname}...")

    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("https://www.pagesjaunes.fr/pagesblanches")

    driver.find_element_by_id("didomi-notice-agree-button").click()
    driver.find_element_by_id("ou").send_keys("Seine-Maritime (76)")
    driver.find_element_by_id("quoiqui").send_keys(lastname)
    driver.find_element_by_xpath("//button[@title='Trouver']").click()

    time.sleep(1)

    # all_names = {}
    while True:
        # # Get people names
        all_names = [(t.text, t.get_attribute("href")) for t in driver.find_elements_by_xpath("//a[contains(@class, 'denomination-links')]") if lastname in t.text.split()[0].lower()]
        print(len(all_names))
        print(all_names[:5])

        # # Get adresses
        # all_adresses = [t.text.split("\n")[0] for t in driver.find_elements_by_xpath("//div[@class='main-adresse-container row-adresse with-adresse']")]
        # print(len(all_adresses))
        # print(all_adresses[:15])

        # # Click on 'see phone numbers'      
        # # for elem in driver.find_elements_by_xpath("//a[@class='phone pj-link']"):
        # for elem in driver.find_elements_by_xpath("//*[contains(text(), 'Afficher le n°')]"):
        #     elem.click()

        # # Then get the phone numbers
        # all_numbers = [t.text for t in driver.find_elements_by_class_name("num")]
        # print(len(all_numbers))
        # print(all_numbers[:15])

        # Click on 'see phone numbers'      
        # for elem in driver.find_elements_by_xpath("//a[@class='phone pj-link']"):
        # for elem in driver.find_elements_by_xpath("//*[contains(text(), 'Afficher le n°') or contains(@class, 'phone')]"):
        #     elem.click()



        try: 
            driver.find_element_by_xpath("//*[@id='pagination-next']").click()
            time.sleep(1)
        except exceptions.NoSuchElementException as e:
            break

    driver.quit()