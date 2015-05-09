from urllib import request, error
from html import parser
from bs4 import BeautifulSoup
import csv, os

CARD_LOG = r'C:/MTG/Log.csv'


with open(CARD_LOG,'r') as file_in, open('C:/TempLog.csv','w',newline='') as file_out:
    # Set up reader and writer
    this_reader = csv.reader(file_in)
    this_writer = csv.writer(file_out)
    this_writer.writerow(['Card','Set Name','Foil?','Median Value'])

    # Iterate through lines in csv, retrieving card and set names and getting their prices
    for row in this_reader:
        # Skip header row
        if row[0] == 'Card': continue

        card = row[0].replace(r"'","").replace(r",","")
        set = row[1]
        foil = row[2]
        original_price = row[3]

        if original_price != "" and original_price != "URL ERROR":
            this_writer.writerow([card,set,foil,original_price])
            continue

        # Check if card is foil
        if foil == 'y': set += r':Foil'

        print("Card: {}     |     Set: {}".format(card,set))

        this_url = "http://www.mtggoldfish.com/price/{}/{}".format(set.replace(' ','+'),card.replace(' ','+'))
        print("Searching URL: {}".format(this_url))

        # Open page, retrieve price; if failed, report error
        try:
            this_page = request.urlopen(this_url)
            page_content = this_page.read()
            this_soup = BeautifulSoup(page_content)
            try:
                price = float(this_soup.find_all('div','price-box-price')[1].string)
            except(IndexError):
                price = float(this_soup.find_all('div','price-box-price')[0].string)
            print("Price found: {}".format(price))
            this_writer.writerow([card,set.split(':')[0],foil,price])
        except(error.HTTPError):
            print("URL Error")
            print("----------------------")
            this_writer.writerow([card,set.split(':')[0],foil,"URL ERROR",original_price])
            continue

        print("----------------------")

# Delete original log and rename new file
os.remove('C:/MTG/Log.csv')
os.rename('C:/MTG/TempLog.csv','C:/MTG/Log.csv')
