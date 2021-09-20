import streamlit as st
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
# import time
import pandas as pd


if __name__ == '__main__':
    st.set_page_config(page_title="Lastname search", layout="wide")

    with st.sidebar.form("Form"):
        lastname = st.text_input('Enter lastname')
        submitted = st.form_submit_button("Submit")


    if submitted:
        with st.spinner(text=f"Search for the lastname '{lastname}' in progress..."):
            lastname = lastname.lower()

            fp = webdriver.FirefoxProfile()
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(firefox_profile=fp, options=options)
            driver.get("https://www.pagesjaunes.fr/pagesblanches")

            driver.find_element_by_id("didomi-notice-agree-button").click()
            driver.find_element_by_id("ou").send_keys("Seine-Maritime (76)")
            driver.find_element_by_id("quoiqui").send_keys(lastname)
            driver.find_element_by_xpath("//button[@title='Trouver']").click()

            all_names = []
            while True:
                # # Get people names
                all_names.extend([(t.get_attribute("title"), t.get_attribute("href")) for t in driver.find_elements_by_xpath("//a[contains(@class, 'denomination')]") if lastname in t.get_attribute("title").split()[0].lower()])
                
                try: 
                    driver.find_element_by_xpath("//*[@id='pagination-next']").click()
                except exceptions.NoSuchElementException as e:
                    break

        # Put data into dataframe
        df = pd.DataFrame(all_names, columns=["Name", "URL"])
        st.dataframe(df)

        driver.quit()