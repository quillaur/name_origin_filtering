import streamlit as st
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

from selenium_search import search_white_pages, search_118712


def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">{text}</a>'

def create_id_from_name_address(fullname: str, address: str) -> str:
    if "," in address:
        address = address.split(",")
        zip_city = address[-1].strip()
        street = address[-2].strip()
        street = street.split()[-1]
        return f"{fullname.strip()} {street} {zip_city}"
    else:
        return f"{fullname.strip()} {address}"


if __name__ == '__main__':
    st.set_page_config(page_title="Lastname search", layout="wide")

    with st.sidebar.form("Form"):
        lastname = st.text_input('Enter lastname')
        submitted = st.form_submit_button("Submit")


    if submitted:
        with st.spinner(text=f"Search for the lastname '{lastname}' in progress..."):
            lastname = lastname.lower()

            # Set driver
            fp = webdriver.FirefoxProfile()
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(firefox_profile=fp, options=options)

            wp_names = search_white_pages(lastname, driver)

            other_names = search_118712(lastname, driver)

            all_names = {}

            for info in wp_names:
                lower_fullname = info[0].lower()
                id_name_address = create_id_from_name_address(lower_fullname, info[1].lower())
                
                all_names[id_name_address] = {
                    "Name": info[0],
                    "Pages Blanches": make_clickable(info[2], "Yes"),
                    "118712": "No",
                    "Forbears": make_clickable(f"https://forebears.io/fr/surnames/{lower_fullname.split()[0]}", "Yes")
                }

            for info in other_names:
                lower_fullname = info[0].lower()
                id_name_address = create_id_from_name_address(lower_fullname, info[1].lower())
                
                if id_name_address in all_names.keys():
                    all_names[id_name_address]["118712"] = make_clickable(info[2], "Yes")
                else:
                    all_names[id_name_address] = {
                    "Name": info[0],
                    "Pages Blanches": "No",
                    "118712": make_clickable(info[2], "Yes"),
                    "Forbears": make_clickable(f"https://forebears.io/fr/surnames/{lower_fullname.split()[0]}", "Yes")
                }      

            driver.quit()

            all_names = [d for k, d in all_names.items()]

            df = pd.DataFrame(all_names)

        # st.dataframe(df)
        st.write(df.to_html(escape = False), unsafe_allow_html = True)

        