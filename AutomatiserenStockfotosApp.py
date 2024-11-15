# packages
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import streamlit as st

# Titel van de applicatie
st.title("Afbeelding downloader")

# Invoerveld voor de URL
url = st.text_input("Geef de URL van VW configurator op:")

# Pad naar de gewenste map om afbeeldingen op te slaan
output_folder = "Downloads_VWconfig"
os.makedirs(output_folder, exist_ok=True)

# Functie om de Selenium WebDriver te configureren en te starten
@st.cache_resource
def get_driver():
    # Configureer de headless Chrome opties
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Gebruik ChromeDriverManager om Chromium te installeren en in te stellen
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

# Knop om het downloaden te starten
if st.button("Download Afbeeldingen"):
    if url:
        st.write("Downloadproces gestart...")
        
        # Start de driver en laad de opgegeven URL
        driver = get_driver()
        driver.get(url)
        
        # Parse de HTML met BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()  # Sluit de driver nadat de pagina is geladen en verwerkt
        
        # Zoek en download alle <img> tags met een bepaalde class
        img_tags = soup.find_all('img', class_='image')
        st.write(f"Gevonden afbeeldingen: {len(img_tags)}")

        # Itereer door elk <img> tag in de lijst
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                img_name = os.path.join(output_folder, img_url.split('/')[-1])
                
                try:
                    urlretrieve(img_url, img_name)
                    st.write(f"Afbeelding gedownload: {img_name}")
                except Exception as e:
                    st.write(f"Fout bij het downloaden van {img_url}: {e}")
    else:
        st.warning("Voer een geldige URL in voordat je op 'Download Afbeeldingen' klikt.")