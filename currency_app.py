from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

#HTTP Post request
@app.route('/', methods=['GET','POST'])
def currency_converter():
    data = request.get_json()
    # using dictionaries to get the required params
    in_curr = data['queryResult']['parameters']['unit-currency']['currency']
    quant = data['queryResult']['parameters']['unit-currency']['amount']
    out_curr = data['queryResult']['parameters']['currency-name']
    
    # get the currency exchange rates from api
    url=f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={in_curr}&to_currency={out_curr}&apikey=9325UQDI0CNBJ4NH'
    response=requests.get(url)
    response=response.json()
    con_fact=float(response['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    final_amt=round(quant*con_fact,2)
    
    push={'fulfillmentText':f'{quant:,} {in_curr} is {final_amt:,} {out_curr}, Exchange Rate: {con_fact}'}
    return jsonify(push)