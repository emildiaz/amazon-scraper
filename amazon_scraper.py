import csv
import requests
from bs4 import BeautifulSoup

#Must change this for your unique user agent
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

#Takes in the item the user inputted and creates the url
def make_url(item):
    #normalize the item for the link
    item_fixed = item.strip().lower().replace(' ', '+')
    url = 'https://www.amazon.com/s?k=' + item_fixed + '&ref=nb_sb_noss_2'
    return url

#Creates the html soup for the created url
def scrape(url):
    page = requests.get(url, headers=HEADERS)
    temp_soup = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(temp_soup.prettify(), 'html.parser')
    return soup

#Gets the given product's name
def get_product_name(product):
    try:
        product_name = product.find('a', {'class':'a-link-normal a-text-normal'}).text.strip()
    except:
        return 'N/A'
    return product_name

#Gets the given product's price
def get_price(product):
    try:
        price = product.find('span', {'class':'a-offscreen'}).text.strip()
    except:
        return 'N/A'
    return price

#Gets the given product's rating
def get_rating(product):
    try:
        rating = product.find('span', {'class':'a-icon-alt'}).text.strip() #[:-15]
    except:
        return 'N/A'
    return rating

#Gets the given product's amazon prime status
def get_prime(product):
        is_prime = product.find('i', {'aria-label':'Amazon Prime'})
        if is_prime != None:
            return True
        return False

def main():
    item = input('Amazonify an item: ')
    url = make_url(item)
    soup = scrape(url)

    #Create a csv writer
    with open('amazon_items.csv', 'w') as csv_file:
        fieldnames = [item.upper() + ' ' + '| Product Names', 'Price', 'Prime', 'Rating']
        csv_writer = csv.DictWriter(csv_file, fieldnames)
        csv_writer.writeheader()

        #Find the products of the user inputted item on amazon
        products = soup.find_all('span', {'cel_widget_id':'MAIN-SEARCH_RESULTS'})

        #Find the unique variables for each available product
        sorted_products = []
        for product in products:
            product_name = get_product_name(product)
            price = get_price(product)
            rating = get_rating(product)
            is_prime = get_prime(product)

            #package up the gathered data and put it in a csv file
            product_summary = {
                                item.upper() + ' ' + '| Product Names' : product_name,
                                'Price' : price,
                                'Prime' : is_prime,
                                'Rating' : rating
                                }
            #Removes all products that do not have prices                    
            if(product_summary['Price'] != 'N/A'):  
                sorted_products.append(product_summary)

        #Sort in lowest to highest price
        sorted_products.sort(key=lambda product:float(product['Price'][1:].replace(',','')))
        for product in sorted_products:
            csv_writer.writerow(product)
    
    print("Done!")
        

if __name__ == "__main__":
    main()
