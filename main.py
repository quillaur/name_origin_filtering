import streamlit as st
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import geckodriver_autoinstaller
from unidecode import unidecode
import requests

from selenium_search import search_white_pages, search_118712


def make_clickable(url: str, text: str) -> str:
    """Create an hyperlink clickable in a streamlit table.

    Args:
        url (str): the url to send the user to uppon clicking.
        text (str): The visible text of the hyperlink.

    Returns:
        str: The clickable hyperlink in html format.
    """
    return f'<a target="_blank" href="{url}">{text}</a>'


def create_id_from_name_address(fullname: str, address: str) -> str:
    """Attempt to create a unique ID to identify an individual given its name and address.
    
    WARNING: This is an attempt because the unicity of this idea has not been fully tested.

    Args:
        fullname (str): The last and firstname of the person separated by a space. 
        address (str): The person's address.

    Returns:
        str: The unique id.
    """
    # Remove accents
    fullname = unidecode(fullname)
    address = unidecode(address)

    if "," in address:
        address = address.split(",")
        zip_city = address[-1].strip()
        street = address[-2].strip()
        street = street.split()[-1]
        return f"{fullname.strip()} {street} {zip_city}"
    else:
        return f"{fullname.strip()} {address}"


def this_forbears_url_exists(url: str, headers: dict) -> bool:
    """This function checks that the created forbears url does not redirect us to the homepage.

    Args:
        url (str): The URL to check. 
        headers (headers): The headers to send with the URL so the HTTP request is constructed by the browser and not python.

    Returns:
        bool: True if the page returned by the request is not the homepage of forbears, else False.
    """
    r = requests.get(url, headers=headers)

    return r.url != "https://forebears.io/"


def create_forbears_url(lastname: str, headers: dict) -> str:
    """Create a URL to get the lastname page on forbears.io.

    Args:
        lastname (str): The lastname to construct the URL with.
        headers (headers): The headers to send with the URL so the HTTP request is constructed by the browser and not python.

    Returns:
        str: The forbears URL.
    """
    url = f"https://forebears.io/fr/surnames/{lastname}"

    if this_forbears_url_exists(url, headers):
        return make_clickable(url, "Yes")
    else:
        return "No"


if __name__ == '__main__':
    # Use the whole size of the page
    st.set_page_config(page_title="Lastname search", layout="wide")

    # The form in which to input the lastname to search for.
    with st.sidebar.form("Form"):
        lastname = st.text_input('Entrez un nom de famille')
        address = st.text_input('Entrez un département, une ville ou une adresse')
        submitted = st.form_submit_button("Ok")


    # st.write("Cette application permet de faire une recherche d'un nom de famille sur 118712 et les pages blanches pour un département donnée.")
    
    if submitted:
        # Keep track of time
        start = time.time()

        # Initiat the search and run a spinner while the search happens.
        with st.spinner(text=f"Recherche du nom de famille '{lastname}' en cours..."):
            # Make everything lower for easier search
            lastname = lastname.lower()
            address = address.lower()

            # Define a header for url existance verification
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


            # Set driver
            geckodriver_autoinstaller.install()
            fp = webdriver.FirefoxProfile()
            options = Options()
            options.headless = True

            # driver = webdriver.Firefox(firefox_profile=fp, options=options, executable_path="/home/appuser/.conda/bin/geckodriver",)
            driver = webdriver.Firefox(firefox_profile=fp, options=options)

            # Search the white pages website
            wp_names = search_white_pages(lastname, address, driver)
            # print(len(wp_names))

            # Search the 118712 website
            other_names = search_118712(lastname, address, driver)
            # print(len(other_names))

            # Store all data in a dict
            all_names = {}
            for info in wp_names:
                lower_fullname = info[0].lower()

                # Create the unique ID for this person
                id_name_address = create_id_from_name_address(lower_fullname, info[1].lower())
                
                all_names[id_name_address] = {
                    "Name": info[0],
                    "Pages Blanches": make_clickable(info[2], "Yes"),
                    "118712": "No",
                    # "Forbears": make_clickable(f"https://forebears.io/fr/surnames/{lower_fullname.split()[0]}", "Yes")
                    "Forbears": create_forbears_url(lower_fullname.split()[0], headers)
                }

            for info in other_names:
                lower_fullname = info[0].lower()
                id_name_address = create_id_from_name_address(lower_fullname, info[1].lower())
                
                # If the person is already in our resul dictionary
                if id_name_address in all_names.keys():
                    # Add the 118712 URL
                    all_names[id_name_address]["118712"] = make_clickable(info[2], "Yes")
                else:
                    # Otherwise, add the person to the dict
                    all_names[id_name_address] = {
                    "Name": info[0],
                    "Pages Blanches": "No",
                    "118712": make_clickable(info[2], "Yes"),
                    # "Forbears": make_clickable(f"https://forebears.io/fr/surnames/{lower_fullname.split()[0]}", "Yes")
                    "Forbears": create_forbears_url(lower_fullname.split()[0], headers)
                }      

            # We don't need the selenium driver anymore
            driver.quit()

            # Format the result as a list of dicts for easier use when creating the dataframe.
            all_names = [d for k, d in all_names.items()]

            # Viewing the results as a dataframe (or table) will be nicer.
            df = pd.DataFrame(all_names)

        if df.empty:
            # Show warning
            st.warning(f"Aucune donnée trouvée pour ce nom de famille: {lastname}")
        else:
            # Show the results
            st.write(df.to_html(escape = False), unsafe_allow_html = True)

        end = time.time()
        timedelta = round(end-start, 2)
        st.sidebar.write(f"La recherche a prit {timedelta} secondes.")