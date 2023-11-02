# -*- coding: utf-8 -*-
"""

Web Scraping CloudSkillsBoost Profile

"""

#Enter Your Google Cloud Skills Boost Public Profile Here
profile_url = "https://www.cloudskillsboost.google/public_profiles/3ef4afa5-0bf9-4b62-b037-bd8f773f947b"

# Installting & Importing all necessary python libraries  to perform the webscraping
pip install beautifulsoup4==4.10.0 pandas==1.4.0 requests==2.26.0

from re import sub
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Fetching the public profile Webpage for the first time & parsing it using beautifulsoup library
response = requests.get(profile_url)
soup = BeautifulSoup(response.text, "html.parser")

#scraping just the Badges 
candidate_name = soup.find('h1', class_='ql-display-small').text.strip()
print(candidate_name)
badges = soup.find_all('span', class_='ql-title-medium l-mts')
badge_names = [badge.text.strip() for badge in badges]
print(" Badges Completed:")
for badge in badge_names:
    print(f"    - {badge}")
