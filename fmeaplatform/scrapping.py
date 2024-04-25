import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://fr.carcarekiosk.com/videos/Acura/CL/1999'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements by div class which typically contains the information
divs = soup.find_all('div', class_='col-md-4 col-sm-6 p-2')

# Iterate through each div and find all <a> tags within
for div in divs:
    a_tags = div.find_all('a')  # Find all <a> tags within each div
    for tag in a_tags:
        if tag.text.strip()!= "":
            if tag['href'] 
            print('URL:', tag['href'])  # Print the href attribute of each <a> tag
            print('Text:', tag.text.strip())  # Print the text of each <a> tag
            print('-------------')
