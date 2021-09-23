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
        all_names = [(t.get_attribute("title"), t.get_attribute("href")) for t in driver.find_elements_by_xpath("//a[contains(@class, 'denomination')]") if lastname in t.get_attribute("title").split()[0].lower()]
        print(len(all_names))
        print(all_names)

        # # Get adresses
        all_adresses = [t.text.split("\n")[0] for t in driver.find_elements_by_xpath("//a[contains(@title, 'Voir le plan')]")]
        print(len(all_adresses))
        print(all_adresses)

        try: 
            driver.find_element_by_xpath("//*[@id='pagination-next']").click()
            time.sleep(1)
        except exceptions.NoSuchElementException as e:
            break


    # driver.get("https://www.118712.fr/")
    # time.sleep(0.5)
    # driver.find_element_by_id("didomi-notice-agree-button").click()
    # # driver.find_element_by_id("search_input_mono").send_keys(f"{lastname}, Seine-Maritime (76)")
    # driver.find_element_by_id("search_input_mono").send_keys(f"rue de Sotteville, 76100 ROUEN")
    # driver.find_element_by_id("search_validation_normal").click()

    # # driver.find_element_by_id("propart-button").click()
    # # driver.find_element_by_id("ui-id-3").click()

    # while True:
    #     try: 
    #         driver.find_element_by_xpath("//*[@id='more']").click()
    #         # time.sleep(1)
    #     except exceptions.NoSuchElementException as e:
    #         break
    #     except exceptions.ElementNotInteractableException as e:
    #         break

    # all_names = [(t.get_attribute("title"), t.get_attribute("href")) for t in driver.find_elements_by_xpath("//a[contains(@id, 'result')]")]
    # # all_names = [(t.get_attribute("title"), t.get_attribute("href")) for t in driver.find_elements_by_xpath("//a") if t.is_displayed() and lastname in t.get_attribute("title").split()[0].lower()]
    # print(len(all_names))
    # print(all_names)        


    # driver.get("https://forebears.io/fr/surnames")
    # time.sleep(0.5)
    # driver.find_element_by_name("q").send_keys(f"Min-Tung")
    # driver.find_element_by_xpath("//button[@class='search-button']").click()

    # prevalence = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[3]/div").get_attribute("title")
    # incidece = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[2]/h5").text
    # print(prevalence)
    # print(incidece)

    # driver.quit()