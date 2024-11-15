import streamlit as st
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin
from urllib.request import urlretrieve

# Titel van de applicatie
st.title("Afbeelding Downloader")

# Invoerveld voor de URL
url = st.text_input("Geef de URL van de VW configurator op:")

# Pad naar de gewenste map om afbeeldingen op te slaan
output_folder = "Downloads_VWconfig"
os.makedirs(output_folder, exist_ok=True)

# Knop om het downloaden te starten
if st.button("Download Afbeeldingen"):
    if url and url.startswith(('http://', 'https://')):
        st.write("Downloadproces gestart...")

        # Instellen van Firefox WebDriver in headless mode
        options = Options()
        options.add_argument("--headless")  # Voer Firefox uit in headless mode voor serveromgevingen
        driver = None  # Initialiseer driver buiten try-except blok

        # Selenium WebDriver instellen met foutafhandeling
        try:
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(url)
            
            # Wacht tot de afbeeldingen geladen zijn
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "image"))
            )

            # Parse de HTML met BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Vind <img> tags
            img_tags = soup.find_all('img', class_='image')
            st.write(f"Gevonden afbeeldingen: {len(img_tags)}")

            # Beperk het aantal afbeeldingen tot bijvoorbeeld 30
            max_images = 30
            img_tags = img_tags[:max_images]
            progress_bar = st.progress(0)

            # Download de afbeeldingen
            for index, img_tag in enumerate(img_tags):
                img_url = img_tag.get('src')
                if img_url:
                    img_url = urljoin(url, img_url)
                    img_name = os.path.join(output_folder, img_url.split('/')[-1])
                    
                    try:
                        urlretrieve(img_url, img_name)
                        st.write(f"Afbeelding gedownload: {img_name}")
                        st.image(img_name, caption=f"Gedownload: {img_name}", use_column_width=True)
                    except Exception as e:
                        st.write(f"Fout bij het downloaden van {img_url}: {e}")
                
                # Update voortgang
                progress_bar.progress((index + 1) / max_images)

        except Exception as e:
            st.error(f"Er is een probleem opgetreden: {e}")
        
        finally:
            # Zorg ervoor dat de driver altijd wordt afgesloten
            if driver:
                driver.quit()

    else:
        st.warning("Voer een geldige URL in die begint met 'http://' of 'https://'.")
