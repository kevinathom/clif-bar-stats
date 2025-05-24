# -*- coding: utf-8 -*-
"""
Define helper functions
"""

# Clean a URL to generate filename
def url_to_filename(url, extension='.html'):
    # Get rid of leading http://
    url = url.split('//')[1]

    # Because the slash '/' and '.' characters are treated
    # as special characters in most file systems, we don't
    # want our filename to contain any of these characters

    # Check whether a character is "alpha-numeric" using
    # .isalnum() and keep only alpha-numeric characters
    # in the filename
    filename = "".join(char for char in url if char.isalnum())

    # Since we'll be saving mostly HTML files, we'll append
    # '.html' to the end of each filename
    filename = filename + extension

    return (filename)


# Download only URLs not in the given directory
#  Import required libraries
import os
import requests
import time

#  Define a realistic user agent
#  See http://www.browser-info.net/useragents
spoofed_ua = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'

def get_html_from_url(url, folder='clif_pages'):
    # We'll first check that the folder exists. If it does
    # not already exist, we'll create the folder in the same
    # location as this notebook.
    if not os.path.exists(folder):
        os.makedirs(folder)

        full_filepath = os.path.join(os.getcwd(), folder)
        print("Created folder at: \n\t{}".format(full_filepath))

    # Use function created above to get a valid filename
    filename = url_to_filename(url)

    # We have to tell Python the EXACT location we want
    # to save the file in. To do this, we will use the
    # os.path.join function which allows you to combine
    # several folders/subfolders and a filename to get
    # the full path where you want to save the file.
    filepath = os.path.join(folder, filename)

    # Check if a file at that path already exists
    if os.path.isfile(filepath):
        # If the file already exists, simply load the
        # HTML that was already downloaded
        with open(filepath, 'r') as file:
            raw_html = file.read()

        print('Retrieved HTML from local file: \n\t{}'.format(filepath))

    else:
        # If a file with this filename does NOT already
        # exist, fetch the URL from the web and save the
        # contents to your computer so it can be retrieved
        # from there the next time you want to access it
        response = requests.get(url, headers={"User-Agent": spoofed_ua})
        raw_html = response.text
        with open(filepath, 'w+') as file:
            file.write(raw_html)

        print('Retrieved HTML from web and saved contents to local file: \n\t{}'.format(filepath))

        # For real requests, don't spam the server; wait n seconds
        time.sleep(2)

    return (raw_html)


"""
List URLs to fetch
"""

# Import required libraries
from bs4 import BeautifulSoup

# Products are listed on https://www.clifbar.com/shop
# Get the Shop page and parse it
shop_html = get_html_from_url('https://www.clifbar.com/shop')
shop_soup = BeautifulSoup(shop_html, features = 'html.parser')

# Get product names and addresses
#  List relevant html chunks
product_chunk = shop_soup.find_all('a', {'class':'flavor-product'})

product_url = []
product_brand_1 = []
product_brand_2 = []
product_name = []
for chunk in product_chunk:
    # Iterate though the html chunk for each product
    # Extract the attributes
    product_url.append('https://www.clifbar.com' + chunk.get('href'))
    product_brand_1.append(chunk.find_all('span')[0].text)
    product_brand_2.append(chunk.find_all('span')[1].text)
    product_name.append(chunk.find('h4').text)


"""
Fetch page content
"""

product_protein = []
#product_price_unit = []
product_ingredients = []
product_vitamin_mineral = []
product_allergens = []
for page in product_url:
    # Iterate through each product page
    # Fetch a product page and parse it
    product_html = get_html_from_url(page)
    product_soup = BeautifulSoup(product_html, features = 'html.parser')

    # Fetch pricing box (first item only--maybe fix for later)
    #price_1_url = product_soup.find('a', {'id':'ui-id-1'}).get('href')
    #price_1_html = get_html_from_url(price_1_url)
    #price_1_soup = BeautifulSoup(price_1_html, features = 'html.parser')

    # Extract relevant data
    try:
        if product_soup.find('p', {'class': 'c-results__nutrition-text'}).text.find('g') >= 0:
            # Test for a protein measure
            product_protein.append(product_soup.find('p', {'class': 'c-results__nutrition-text'}).text.split('g')[0])
        else:
            product_protein.append('NA')
    except:
        # In case there is nothing is listed
        product_protein.append('NA')
    #product_price_unit.append(price_1_soup.find('div', {'class':'line-two'}))
    product_ingredients.append(product_soup.find_all('p', {'class':'c-nutrition__container__description'})[0].text[:-1].lower())
    try:
        product_allergens.append(product_soup.find_all('p', {'class':'c-nutrition__container__description'})[2].text[9:].lower().split('. may contain')[0])
        product_vitamin_mineral.append(product_soup.find_all('p', {'class': 'c-nutrition__container__description'})[1].text[:-1].lower())
    except:
        try:
            product_allergens.append(product_soup.find_all('p', {'class': 'c-nutrition__container__description'})[1].text[9:].lower().split('. may contain')[0])
            product_vitamin_mineral.append('NA')
        except:
            # In case there is nothing is listed
            product_allergens.append('NA')
            product_vitamin_mineral.append('NA')


"""
Consolidate and export data
"""

# Import required libraries
from pandas import DataFrame

# Create a dataframe
clif_products = {'Brand_1': product_brand_1,
                 'Brand_2': product_brand_2,
                 'Name': product_name,
                 'Protein': product_protein,
                 'Ingredients': product_ingredients,
                 'Vitamin_Mineral': product_vitamin_mineral,
                 'Allergens': product_allergens}

df = DataFrame(clif_products, columns = ['Brand_1', 'Brand_2', 'Name', 'Protein', 'Ingredients', 'Vitamin_Mineral', 'Allergens'])

# Export to csv
df.to_csv(r'clif_products.csv')