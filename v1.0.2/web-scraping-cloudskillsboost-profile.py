# -*- coding: utf-8 -*-
"""
Web Scraping CloudSkillsBoost Profile  V1.0.2
This was originally build to work in Google Colab.
This script is generated using Google Colaboratory Export for documenting on Github.
Original Colab file made by Author is kept private 
If you are using this code, please give credits and maybe put a star on the repo. Thanks. 
"""

# Installting & Importing all necessary python libraries  to perform the webscraping
!pip install beautifulsoup4==4.10.0 pandas==1.4.0 requests==2.26.0
from re import sub
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Upload the daily-report CSV you receive from Google Cloud as a facilitator to the runtime
#give the location to the csv here. in my case, the csv was saved at /content/GCSB-Scrape/daily-report.csv
data = pd.read_csv("v1.0.2/daily-report.csv")

# Replace this section with the badges name that are required for your candidates to complete in order to finish the event.
VALID_BADGES = [
    "Level 3 GenAI: Prompt Engineering",
    "Google Cloud Computing Foundations: Cloud Computing Fundamentals",
    "Google Cloud Computing Foundations: Infrastructure in Google Cloud",
    "Google Cloud Computing Foundations: Networking & Security in Google Cloud",
    "Google Cloud Computing Foundations: Data, ML, and AI in Google Cloud",
    "Create and Manage Cloud Resources",
    "Perform Foundational Infrastructure Tasks in Google Cloud",
    "Build and Secure Networks in Google Cloud",
    "Perform Foundational Data, ML, and AI Tasks in Google Cloud"
]

#cleaning and modifiying csv data to better conform with existing code variables and to remove Blank Lines.
data['Institution'].isnull().sum()
data.dropna(subset=['Institution'], inplace=True)
data.rename(columns = {'Google Cloud Skills Boost Profile URL':'profile_url','Student Name':'name'}, inplace = True)

#printing the csv data details
print("-" * 60)
print(data.info(verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None))
#print("-" * 60)
#print(data.describe())
print("-" * 60)
print(data.head())
print("-" * 60)


# Now for the Bulk Processing part.. The script will go through each row in the csv and fetch each public profile one by one using beautifulsoup
# student variable keeps track on total eligible students based on above given valid badges list.

student = 0
rows = []
AllCompletedCount = 0
for row in data.itertuples():
    print("-" * 60)
    student +=1
    completed_badges = []
    num_completed_badges = 0
    print("Scrapping Student No {} \n".format(student))
    name = row.name
    profile_url = row.profile_url
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

    # this section will cross check each badge to the badge that is valid for the event mentioned above. 
    completed_badges = [badge for badge in badge_names if badge in VALID_BADGES]
    num_completed_badges = len(completed_badges)
    completion_status = f"{candidate_name} has completed {num_completed_badges} out of {len(VALID_BADGES)} valid badges."
    print(completion_status)

    # change the 9 to however much your eligibility badge count is. 
    if num_completed_badges >= 9:
      AllCompletedCount += 1
    # create a result.txt file in the same location as daily-report.csv to save the logs. The script does not check for file and will crash. I will fix it soon. I was on a hurry to complete this script before the event ended. 
    with open("v1.0.2/result.txt", "a") as file:
      file.write(completion_status + "\n")
    # Restarting Loop for next student till all rows are finished.

print("-" * 80)
print("-" * 80)
print("Total Students who completed 9 Eligible Labs are : {}".format(AllCompletedCount))
print("-" * 80)
print("-" * 80)

#made by @arjunraghunandanan
#www.arjunraghunandanan.com
#02-Nov-2023
