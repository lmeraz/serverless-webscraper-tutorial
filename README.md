# A Serverless Webscraping Tutorial
Scrape the Amazon [Alexa Voice Deals](https://www.amazon.com/b?node=16924218011) meta data on a daily basis using a serverless infrastructure.

### Set Up
Tutorial assumes AWS CLI is installed and credentials are properly set up in `~/.aws/credentials`.
Tutorial also assumes S3, API Gateway, DynamoDB, and Lambda are available in the region found in `~/.aws/config`. See [Configuring the AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) for more details.
### Install pipenv
If you haven't already, pip install pipenv. It's awesome!
```
pip3 install pipenv
```
### Clone the repo
```
git clone git@github.com:lmeraz/serverless-webscraper.git
```
### Install virutal environment
pipenv installs all the packages needed, in this case, zappa and lmxl. In the project folder do:
```
pipenv install
```
### Create a DynamoDB table
DynamoDB will store the data. Replace `MyTableName` with your desired table name.
```
aws dynamodb create-table \
    --table-name MyTableName \
    --attribute-definitions \
        AttributeName=Date,AttributeType=S \
        AttributeName=ProductID,AttributeType=S \
    --key-schema AttributeName=Date,KeyType=HASH AttributeName=ProductID,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
```
### Create a .env file
The module uses environment variables to operate locally and on lambda.
Create a .env with the following. Replace table `MyTableName` with your dynamodb table.
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
### Create an S3 bucket
Create an S3 Bucket. Replace `my-bucket-name` with your bucket name. The bucket stores our module.
```
aws s3 mb s3://my-bucket-name
```
In zappa_settings.json replace `my-bucket-name` with your bucket name
### Test locally
Start the virtualenv
```
pipenv shell
```
Run the module.
```
python app.py
```
### Deploy
Deploy the module
```
zappa deploy dev
```
Finally, set up set up the [environment variables](http://docs.aws.amazon.com/lambda/latest/dg/env_variables.html) in the AWS Lambda console.
