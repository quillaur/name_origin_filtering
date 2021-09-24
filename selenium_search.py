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



def search_white_pages(lastname: str, driver: webdriver) -> list:
    driver.get("https://www.pagesjaunes.fr/pagesblanches")
    driver.find_element_by_id("didomi-notice-agree-button").click()
    driver.find_element_by_id("ou").send_keys("Seine-Maritime (76)")
    driver.find_element_by_id("quoiqui").send_keys(lastname)
    driver.find_element_by_xpath("//button[@title='Trouver']").click()

    time.sleep(0.5)

    all_names = []
    while True:
        for indi in driver.find_elements_by_xpath("//li"):
            try:
                name_elem = indi.find_element_by_xpath(".//a[contains(@class, 'denomination')]")
            except exceptions.NoSuchElementException:
                continue
            
            fullname = name_elem.get_attribute("title")

            adress_elem = indi.find_element_by_xpath(".//a[contains(@title, 'Voir le plan')]")

            if lastname in fullname.lower():
                all_names.append((fullname, adress_elem.text.split("\n")[0], name_elem.get_attribute("href")))

        try: 
            driver.find_element_by_xpath("//*[@id='pagination-next']").click()
            time.sleep(0.5)
        except exceptions.NoSuchElementException as e:
            break

    return all_names


def search_118712(lastname: str, driver: webdriver) -> list:
    driver.get("https://www.118712.fr/")
    time.sleep(0.5)
    driver.find_element_by_id("didomi-notice-agree-button").click()
    driver.find_element_by_id("search_input_mono").send_keys(f"{lastname}, Seine-Maritime (76)")
    driver.find_element_by_id("search_validation_normal").click()

    while True:
        try: 
            driver.find_element_by_xpath("//*[@id='more']").click()
        except exceptions.NoSuchElementException as e:
            break
        except exceptions.ElementNotInteractableException as e:
            break

    all_names = []
    for indi in driver.find_elements_by_xpath("//article"):
        name_elem = indi.find_element_by_xpath(".//a[contains(@id, 'result')]")
        fullname = name_elem.get_attribute("title")

        adress_elem = indi.find_element_by_xpath(".//div[@class='address']")

        if lastname in fullname.lower():
            all_names.append((fullname, adress_elem.text, name_elem.get_attribute("href")))

    return all_names



if __name__ == '__main__':
    ###################
    #### Arguments ####
    ###################
    args = docopt(__doc__)

    lastname = args["--lastname"].lower()
    print(f"Searching for {lastname}...")

    fp = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=fp)
    
    all_names = search_white_pages(lastname, driver)
    # all_names = search_118712(lastname, driver)   

    print(len(all_names))
    print(all_names) 

    for n in all_names:
        name = n[0].split()
        l = name[0]
        f = " ".join(name[1:])
        address = n[1].split(",")
        zip_city = address[-1].strip()
        street = address[-2].strip()
        street = street.split()[-1]
        print(f"lastname: {l}, firstname: {f}, street: {street}, zip_city: {zip_city}")
        id_address = f"{n[0]} {street} {zip_city}"
        print(id_address)



    # driver.get("https://forebears.io/fr/surnames")
    # time.sleep(0.5)
    # driver.find_element_by_name("q").send_keys(f"Min-Tung")
    # driver.find_element_by_xpath("//button[@class='search-button']").click()

    # prevalence = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[3]/div").get_attribute("title")
    # incidece = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[2]/h5").text
    # print(prevalence)
    # print(incidece)

    # driver.quit()