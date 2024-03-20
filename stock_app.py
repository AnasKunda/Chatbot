# Importing the required libraries
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)
from datetime import date
import datetime
from datetime import timedelta
import pytz

# Getting the current time in NYC
tz_NY = pytz.timezone('America/New_York') 
datetime_NY = datetime.datetime.now(tz_NY).time()
today = date.today()


stock_dictionary={'Apple, INC.':'AAPL','Google':'GOOGL','Microsoft':'MSFT','Facebook':'META','Amazon':'AMZN',
                  'Samsung Electronics':'SSNLF','Synopsys, INC.':'SNPS','IBM':'IBM','Tesla':'TSLA','Intel Corporation':'INTC', 'NVIDIA Corp':'NVDA'}

# HTTP POST Request
@app.route('/', methods=['GET','POST'])
def stock_search():
    data=request.get_json()
    company=data['queryResult']['parameters']['company']
    
    # Checking if the market is open and then fetching the statistics. 
    if (datetime_NY <= datetime.time(16,0,0)) and (datetime_NY >=datetime.time(9,30,0)):
            url=f'https://realstonks.p.rapidapi.com/{stock_dictionary[company]}'
            headers = {
                "X-RapidAPI-Key": "17264f8dbbmsh73e427a3cc86712p19c225jsnbd56a2a722a2",
                "X-RapidAPI-Host": "realstonks.p.rapidapi.com"}

            stock_response=requests.get(url,headers=headers)
            stock_response= stock_response.json()
            price=stock_response['price']
            change_point=stock_response['change_point']
            change_percentage=stock_response['change_percentage']
            total_vol=stock_response['total_vol']
            push={'fulfillmentText':f'''Current Stock Statistics for {company}\n
            Price: {price}\n
            Change Point: {change_point}\n
            Change Percentage: {change_percentage}\n
            Total Volume: {total_vol}'''}
            return jsonify(push)
    # If the market is closed then fetch the data from another api. 
    else:
    # This checks if the timeframe is today or not, if not it displays the message 'I can't do that yet'
        date_time=data['queryResult']['parameters']['date-time']
        dt=''
        if date_time[:10]==str(today):
            dt=str(today)
        elif date_time[:10]=='':
            dt=str(today)
        elif any('endDate' in i for i in date_time):
            return jsonify({'fulfillmentText':'I can\'t do that yet'})
        else:
            pass
        url=f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_dictionary[company]}&apikey=9325UQDI0CNBJ4NH'
        stock_response=requests.get(url)
        stock_response= stock_response.json()
        stock_data=stock_response['Time Series (Daily)'][dt]
        opening=stock_data['1. open']
        high=stock_data['2. high']
        low=stock_data['3. low']
        closing=stock_data['4. close']
        volume=stock_data['5. volume']
        push={'fulfillmentText':f'''Today's Stock Statistics for {company} on {str(today)} (All prices in USD)\n
        Opening Price: {opening}\n
        High Price: {high}\n
        Low Price: {low}\n
        Closing Price: {closing}\n
        Volume: {int(volume):,}'''}
        return jsonify(push)