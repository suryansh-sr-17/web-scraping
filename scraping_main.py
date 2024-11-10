from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def get_product_details(product_url: str) -> dict:
    product_details = {}

    # Create a Service object and specify the path to chromedriver
    service = Service(r"C:\Users\Suryansh SR\Desktop\SuryanshSR\Projects\chromedriver-win64\chromedriver.exe")  # Replace with your path
    driver = webdriver.Chrome(service=service)

    driver.get(product_url)
    time.sleep(3)  # Wait for the page to fully load

    soup = BeautifulSoup(driver.page_source, 'lxml')

    try:
        # Extract product title
        title_tag = soup.find('span', attrs={'id': 'productTitle'})
        if title_tag:
            title = title_tag.get_text().strip()
            product_details['title'] = title
        else:
            print("\nProduct title not found.")

        # Extract product price
        price_symbol_tag = soup.find('span', class_='a-price-symbol')
        price_whole_tag = soup.find('span', class_='a-price-whole')
        price_fraction_tag = soup.find('span', class_='a-price-fraction')

        if price_symbol_tag and price_whole_tag:
            currency_symbol = price_symbol_tag.get_text().strip()
            price_whole = price_whole_tag.get_text().strip()
            price_fraction = price_fraction_tag.get_text().strip() if price_fraction_tag else '00'
            price = f"{currency_symbol}{price_whole}{price_fraction}"
            product_details['price'] = price
        else:
            print("Price not found.")

        product_details['product_url'] = product_url

    except Exception as e:
        print('Could not fetch product details')
        print(f'Failed with exception: {e}')

    driver.quit()
    return product_details if product_details else None

product_url = input('Kindly enter the product url you wish to fetch details from: ')
product_details = get_product_details(product_url)

# Print the output in a more readable format
if product_details:
    print('\nProduct Name:', product_details.get('title', 'N/A'))
    print('Product Price:', product_details.get('price', 'N/A'))
    print('\n')
else:
    print("\nNo product detected!!!\n")
