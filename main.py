import pandas as pd
import re
import numpy as np
import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import date, timedelta
from twilio.rest import Client


# Load Environment Varaibles
load_dotenv(find_dotenv(usecwd=True), override=True)
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


# Define Endpoint, API Key, and Stock Name from Environment Variables
url = os.getenv("STOCK_ENDPOINT")
api_key = os.getenv("ALPHAVANTAGE_API_KEY")
stock = os.getenv("STOCK_NAME")

# Define Prams for API Request to Alpha Vantage
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': stock,
    'apikey': api_key
}

# Make API Request to Alpha Vantage and Get JSON Response
r = requests.get(url, params=params)
data = r.json()

# Get Daily Data from JSON Response from Alpha Vantage API
daily_data = data['Time Series (Daily)']

# Turn the data into a list of dictionaries
data_list = [value for (key, value) in daily_data.items()]

# Get Yesterday's Date and Day Before Yesterday's Date
yesterday_data = data_list[0]
print(yesterday_data)
day_before_data = data_list[1]
print(day_before_data)

# Get Yesterday's Close and Day Before Yesterday's Close
yesterday_close = float(yesterday_data["4. close"])
print(yesterday_close)
day_before_close = float(day_before_data["4. close"])
print(day_before_close)


# Calculate the absolute value of the difference between yesterday's close and the day before yesterday's close
difference = yesterday_close - day_before_close

# Determine if the stock price went up or down
up_down = None

if difference > 0:
    up_down = "🔺" 
else:
    up_down = "🔻"


# Calculate the percentage difference between yesterday's close and the day before yesterday's close
pct_diff = round(difference/ (yesterday_close) * 100)
print(pct_diff)

# If the percentage difference is greater than 5%, get news articles related to the company
news_api_key = os.getenv("NEWS_API_KEY")
company_name = os.getenv("COMPANY_NAME")
news_url = 'https://newsapi.org/v2/everything?'

if abs(pct_diff) > -10:

 #   Define Params for API Request to News API
    news_params = {
        'qInTitle': company_name, 
        'apiKey': news_api_key,
}
# Make API Request to News API and Get JSON Response
news_response = requests.get(news_url, params=news_params)
articles = news_response.json()['articles']


# Use Slicing notations to get the first 3 articles from the JSON response
three_articles = articles[:3]

# Create a new list of the first 3 articles headline and descripton using list comprehension
    
formatted_articles = [f"{stock}: {up_down}: {pct_diff}%\n: Headline: {article['title']}. \nBrief: {article ['description']}" for article in three_articles]

# Initialize Twilio Client and env variables    
twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
my_phone_number = os.getenv("MY_PHONE_NUMBER")
client = Client(twilio_sid, twilio_auth_token)

# Send each article as a separate message via Twilio. 

for article in formatted_articles:

    message = client.messages.create(
        body=article,
        from_=twilio_phone_number,
        to=my_phone_number
    )


# #Optional TODO: Format the message like this: 
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
# """

