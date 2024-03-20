from flask import Flask, jsonify, request
import requests
app = Flask(__name__)
from datetime import timedelta, date
today=date.today()
yesterday=today-timedelta(days=1)

@app.route('/', methods=['GET','POST'])
def news_fetcher():
        data=request.get_json()
        company=data['queryResult']['parameters']['company']
        url=f'https://newsapi.org/v2/everything?q={company}&from={str(yesterday)}&to={str(today)}&sortBy=popularity&apiKey=49c12b1e52544e0c9df67db8f7626392'
        article_response=requests.get(url)
        article_response= article_response.json()
        news_article=''
        for i in range(len(article_response['articles']))[:10]:
            title=article_response['articles'][i]['title']
            url=article_response['articles'][i]['url']
            news_article=news_article+f'''{title}\n{url}\n\n'''
        push={'fulfillmentText':news_article}
        return jsonify(push)