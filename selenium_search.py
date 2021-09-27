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



def search_white_pages(lastname: str, address: str, driver: webdriver) -> list:
    """Search white pages website for/with the given parameters.

    Args:
        lastname (str): The lastname to search for. 
        driver (webdriver): The selenium webdriver to use to automate the search.

    Returns:
        list: The list of names, addresses and URLs that matched the searched lastname.
    """
    driver.get("https://www.pagesjaunes.fr/pagesblanches")
    time.sleep(1)
    driver.find_element_by_id("didomi-notice-agree-button").click()
    time.sleep(1)
    # Seine-Maritime (76)
    driver.find_element_by_id("ou").send_keys(address)
    driver.find_element_by_id("quoiqui").send_keys(lastname)
    driver.find_element_by_xpath("//button[@title='Trouver']").click()

    # Give time for the page to load.
    time.sleep(1)

    # Store results in list
    all_names = []

    # Search as long as possible
    while True:

        # If one element is stale, restart from the while loop.
        # This bool keeps track of stale element.
        stale = False

        # For all elem of the list of search result on this page
        for indi in driver.find_elements_by_xpath("//li"):
            # Try to find a name (in a 'a' tag)
            try:
                name_elem = indi.find_element_by_xpath(".//a[contains(@class, 'denomination')]")
            except exceptions.NoSuchElementException:
                # Go to the next element
                continue
            except exceptions.StaleElementReferenceException as e:
                print(f"I got the stale error: {e}")
                driver.refresh()
                stale = True
                time.sleep(1)
                break
            
            fullname = name_elem.get_attribute("title")

            try:
                adress_elem = indi.find_element_by_xpath(".//a[contains(@title, 'Voir le plan') or contains(@title, 'Itinéraire vers')]")
            except exceptions.NoSuchElementException:
                # Go to the next element
                continue
            except exceptions.StaleElementReferenceException as e:
                print(f"I got the stale error: {e}")
                driver.refresh()
                stale = True
                time.sleep(1)
                break

            # In the case where only the address is given, we want all names returned.
            if not lastname:
                all_names.append((fullname, adress_elem.text.split("\n")[0], name_elem.get_attribute("href")))

            elif lastname in fullname.lower():
                # Store match in a tuple: (full name, address, URL) and append to the final resulting list
                all_names.append((fullname, adress_elem.text.split("\n")[0], name_elem.get_attribute("href")))

        if not stale:
            # If you can't find/click the 'next' button, then break the while loop/search.
            try: 
                driver.find_element_by_xpath("//*[@id='pagination-next']").click()
                time.sleep(0.5)
            except exceptions.NoSuchElementException as e:
                break

    return all_names


def search_118712(lastname: str, address: str, driver: webdriver) -> list:
    driver.get("https://www.118712.fr/")
    time.sleep(1)
    driver.find_element_by_id("didomi-notice-agree-button").click()
    time.sleep(1)
    driver.find_element_by_id("search_input_mono").send_keys(f"{lastname}, {address}")
    driver.find_element_by_id("search_validation_normal").click()
    time.sleep(1)

    while True:
        try: 
            driver.find_element_by_xpath("//*[@id='more']").click()
            time.sleep(1)
        except exceptions.NoSuchElementException as e:
            break
        except exceptions.ElementNotInteractableException as e:
            break

    all_names = []
    for indi in driver.find_elements_by_xpath("//article"):
        name_elem = indi.find_element_by_xpath(".//a[contains(@id, 'result')]")
        fullname = name_elem.get_attribute("title")

        adress_elem = indi.find_element_by_xpath(".//div[@class='address']")

        # In the case where only the address is given, we want all names returned.
        if not lastname:
            all_names.append((fullname, adress_elem.text, name_elem.get_attribute("href")))
        elif lastname in fullname.lower():
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

    # address = "Seine-Maritime (76)"
    address = "seine-maritime"
    
    # Search the white pages website
    # wp_names = search_white_pages(lastname, address, driver)
    # print(len(wp_names))
    # print(wp_names)

    # Search the 118712 website
    other_names = search_118712(lastname, address, driver)
    print(len(other_names))
    print(other_names)

    # for n in wp_names:
    #     name = n[0].split()
    #     l = name[0]
    #     f = " ".join(name[1:])
    #     address = n[1].split(",")
    #     zip_city = address[-1].strip()
    #     street = address[-2].strip()
    #     street = street.split()[-1]
    #     print(f"lastname: {l}, firstname: {f}, street: {street}, zip_city: {zip_city}")
    #     id_address = f"{n[0]} {street} {zip_city}"
    #     print(id_address)



    # driver.get("https://forebears.io/fr/surnames")
    # time.sleep(0.5)
    # driver.find_element_by_name("q").send_keys(f"Min-Tung")
    # driver.find_element_by_xpath("//button[@class='search-button']").click()

    # prevalence = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[3]/div").get_attribute("title")
    # incidece = driver.find_element_by_xpath("/html/body/section/div[2]/div[3]/a[1]/div/div/div[2]/h5").text
    # print(prevalence)
    # print(incidece)

    # driver.quit()