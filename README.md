# A Serverless Webscraper
Scrape a single page on a schedule using a serverless backend

## Set Up
This assumes AWS credentials are properly set up and S3, API Gateway, DynamoDB, and lambda are available in the region found in AWS config.
### Install pipenv
If you haven't already pip install pipenv
```
pip3 install pipenv
```
### Clone the repo
```
git clone git@github.com:lmeraz/serverless-webscraper.git
```
### Install virutal environment
In the project folder
```
pipenv install
```
### Create a .env file
Create a .env with the following
```
target_url = https://www.amazon.com/b?node=16924218011
proxy = {"http": "http://202.159.203.71:80"}
timeout = 5
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
container_query = //ul[@class='promotion-list']//li[@class='promotion']//span[@class='promotion-detail']
title_query = //span[@class='title']/text()
final_price_query = //span[@class='final-price-display-string']/text() 
buy_price_query = //span[@class='buy-price']/text()
utterance_query = //span[@class='golden-utterance-content']/text()
href_query = //a/@href
img_query = //img/@src
table = MyTableName
```
### Create AWS Resources
Create a DynamoDB Table with a Date and ProductID string hash and sort key
In .env replace MyTableName with your table name
Create an S3 Bucket
In zappa_settings.json replace serverless-webscraper-619 with your bucket name

### Deploy
You're ready to rock!
```
zappa deploy dev
```
All done!