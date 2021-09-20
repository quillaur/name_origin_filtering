import streamlit as st
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd


def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">{text}</a>'


if __name__ == '__main__':
    st.set_page_config(page_title="Lastname search", layout="wide")

    with st.sidebar.form("Form"):
        lastname = st.text_input('Enter lastname')
        submitted = st.form_submit_button("Submit")


    if submitted:
        with st.spinner(text=f"Search for the lastname '{lastname}' in progress..."):
            lastname = lastname.lower()

            all_names = {}

            # Set driver
            fp = webdriver.FirefoxProfile()
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(firefox_profile=fp, options=options)

            driver.get("https://www.pagesjaunes.fr/pagesblanches")
            driver.find_element_by_id("didomi-notice-agree-button").click()
            driver.find_element_by_id("ou").send_keys("Seine-Maritime (76)")
            driver.find_element_by_id("quoiqui").send_keys(lastname)
            driver.find_element_by_xpath("//button[@title='Trouver']").click()

            while True:
                # Get people names                
                for elem in driver.find_elements_by_xpath("//a[contains(@class, 'denomination')]"):
                    person_name = elem.get_attribute("title")
                    lower_name = person_name.lower()
                    if lastname in lower_name.split()[0]:
                        all_names[lower_name] = {
                            "Name": person_name,
                            "URL Pages Blanches": make_clickable(elem.get_attribute("href"), "here"),
                            "URL 118712": None
                        }

                try: 
                    driver.find_element_by_xpath("//*[@id='pagination-next']").click()
                except exceptions.NoSuchElementException as e:
                    break


            driver.get("https://www.118712.fr/")
            time.sleep(0.5)
            driver.find_element_by_id("didomi-notice-agree-button").click()
            driver.find_element_by_id("search_input_mono").send_keys(f"{lastname}, Seine-Maritime (76)")
            driver.find_element_by_id("search_validation_normal").click()

            for elem in driver.find_elements_by_xpath("//a[contains(@id, 'result')]"):
                person_name = elem.get_attribute("title")
                lower_name = person_name.lower()
                if elem.is_displayed() and lastname in lower_name.split()[0]:
                    if lower_name in all_names.keys():
                        all_names[lower_name]["URL 118712"] = make_clickable(elem.get_attribute("href"), "here")
                    else:
                        all_names[lower_name] = {
                            "Name": person_name,
                            "URL Pages Blanches": None,
                            "URL 118712": make_clickable(elem.get_attribute("href"), "here")
                        }



            driver.quit()

            all_names = [d for k, d in all_names.items()]

            df = pd.DataFrame(all_names)

        # st.dataframe(df)
        st.write(df.to_html(escape = False), unsafe_allow_html = True)

        