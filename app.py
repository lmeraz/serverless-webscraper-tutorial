import requests
from lxml import html
import os
from datetime import datetime
import boto3
import ast

# Request constants
TARGET_URL = os.environ['target_url']  # Target url of to scrape
PROXY = ast.literal_eval(os.environ['proxy'])  # Proxy to use
TIMEOUT = int(os.environ['timeout'])  # Timeout to use
HEADER = ast.literal_eval(os.environ['header']) # Header to use

# Query Constants
CONTAINER_QUERY = os.environ['container_query']
TITLE_QUERY = CONTAINER_QUERY + os.environ['title_query']
FINAL_PRICE_QUERY = CONTAINER_QUERY + os.environ['final_price_query']
BUY_PRICE_QUERY = CONTAINER_QUERY + os.environ['buy_price_query']
UTTERANCE_QUERY = CONTAINER_QUERY + os.environ['utterance_query']
HREF_QUERY = CONTAINER_QUERY + os.environ['href_query']
IMG_QUERY = CONTAINER_QUERY + os.environ['img_query']

# DynamoDB Constants
TABLE = os.environ['table']

# Services
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE)


def scrape(time):
    '''
    Scraper
    '''
    html_doc = get_html(url=TARGET_URL, proxies=PROXY, timeout=TIMEOUT,
        headers=HEADER)
    titles = find_elements(html_doc, TITLE_QUERY)
    final_prices = find_elements(html_doc, FINAL_PRICE_QUERY)
    buy_prices = find_elements(html_doc, BUY_PRICE_QUERY)
    utterances = find_elements(html_doc, UTTERANCE_QUERY)
    hrefs = find_elements(html_doc, HREF_QUERY)
    imgs = find_elements(html_doc, IMG_QUERY)
    items = [{"date": time, "productID":val[4][4:], "title":val[0],
    "final_price":val[1], "buy_price":val[2],
    "utterance":val[3], "href":val[4], "img":val[5]} for val in zip(titles,
    final_prices, buy_prices, utterances, hrefs, imgs)]
    return items

def find_elements(html, query):
    return html.xpath(query)

def get_html(url, proxies, timeout, headers):
    page = requests.get(url, proxies=proxies, timeout=timeout, headers=headers)
    return html.fromstring(page.content)

def write_to_dynamo(items, table):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

def main():
    data = scrape(str(datetime.now()))
    write_to_dynamo(data, table)

def lambda_handler(event, context):
    print('Checking {} at {}...'.format(TARGET_URL, event['time']))
    try:
        main()
        raise Exception('Main failed')
    except:
        print('Scrape failed!')
        raise
    else:
        print('Scrape succeeded!')
        return event['time']
    finally:
        print('Scrape complete at {}'.format(str(datetime.now())))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()