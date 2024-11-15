# imports and setup code remain the same
import streamlit as st
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        # Selenium WebDriver instellen met foutafhandeling
        driver = None  # Voeg deze regel toe om driver buiten de try-except beschikbaar te maken
        try:
            driver = webdriver.Chrome()
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

            # Beperk het aantal afbeeldingen tot bijvoorbeeld 10
            max_images = 10
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
            if driver:
                driver.quit()  # Dit zorgt ervoor dat driver.quit() alleen wordt aangeroepen als driver bestaat
    else:
        st.warning("Voer een geldige URL in die begint met 'http://' of 'https://'.")
