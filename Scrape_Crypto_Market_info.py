from attr import attr, attrs
import pandas as pd
import requests
from bs4 import BeautifulSoup




#store the date
date = []


def scrape_date():
    scrape_date_URL = 'https://coinmarketcap.com/historical/'
    webpage = requests.get(scrape_date_URL)
    soup = BeautifulSoup(webpage.text,'html.parser')

    tag = soup.select('div.sc-1g0buhb-0.dMscHQ a')
    for i in range(len(tag)):
        date.append(tag[i]['href'])

#create a function to scrape the data
def scrape(date):
    #the website want to scrape
    URL = 'https://coinmarketcap.com/'+date
    webpage = requests.get(URL)
    #Parse the text from websitecmc-table-row
    soup = BeautifulSoup(webpage.text,'html.parser')
    #creat empyty list to store data
    crypto_name_list = []
    crypto_marketcap_list = []
    crypto_price_list = []
    crypto_circulation_supply_list = []
    crypto_symbol_list = []
    #get the table row of element
    tr = soup.find_all('tr',attrs={'class':'cmc-table-row'})
    #create a count variable for the number of crypto currencies that we want to scrape
    count = 0
    #loop through every row to gather the data / information
    for row in tr:
        #check the number reach to top10
        if count == 10:
            break
        count = count + 1

        #store the name of the crypto currency into variable
        #find td element to later get crypto name
        name_col = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'})
        crypto_name = name_col.find('a',attrs={'class':'cmc-table__column-name--name cmc-link'}).text.strip()

        #store the name of the crypto market cap
        #find td element to get cryto marketcap
        crypto_market_cap = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip()
        #find and store the price
        crypto_price  = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip()
        #find circulation supply and symbol
        crypto_circulation_supply_and_symbol= row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).text.strip()
        #Split the data
        crypto_circulaing_supply = crypto_circulation_supply_and_symbol.split(' ')[0]
        crypto_symbol = crypto_circulation_supply_and_symbol.split(' ')[1]

        #Append the data
        crypto_name_list.append(crypto_name)
        crypto_marketcap_list.append(crypto_market_cap)
        crypto_price_list.append(crypto_price)
        crypto_circulation_supply_list.append(crypto_circulaing_supply)
        crypto_symbol_list.append(crypto_symbol)

    #create a empty dataframe to help organize data
    df = pd.DataFrame()
    df['Name'] = crypto_name_list
    df['Market Cap'] = crypto_marketcap_list
    df['Price'] = crypto_price_list
    df['Circulating Supply'] = crypto_circulation_supply_list
    df['Symbol'] = crypto_symbol_list
    print(df)
    #reset dataframe
    df = pd.DataFrame()

#Run the scrape function
scrape_date()


#for loop print(top 10 crypto currencies)
for i in date:
    scrape(i)
















