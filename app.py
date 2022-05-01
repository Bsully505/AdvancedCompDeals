from flask import Flask,render_template,request
from dotenv import load_dotenv
import json
import requests
from html.parser import HTMLParser




# instantiate Slack client
load_dotenv()




App=Flask(__name__)

@App.route('/GetRestResponse',methods=['GET'])
def getResponse():
    query = request.args.get('keyWord')
    Time = request.args.get('time')
    callResponse = CallAPI(query,10)
    res = ParseHTML(callResponse.text)
    #parse req.text and then send back 
    return res
    
    #this is where we are going to get the request command and then return the json responce 
    

#Henoks part is to parse using req test and be able to send it to front end 
def ParseHTML(str):
    # use this library to parse out the desired items HTMLParser 
    # and then return the html 
    reader = HTMLParser()
    reader.feed(str)
    return str


#this is to determine how many calls we need to send out to dealsea with increments of 10 
def DetermineAmtOfCalls(totalNum):
    res = totalNum/10
    res+=1
    return res
        
        
def CallAPI(query, startIndex):
    headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36'}
    req = requests.get(f'https://dealsea.com/search?search_mode=Deals&q={query}&n={startIndex}',headers= headers)
    return req

    



@App.route('/')
def index():
    
    return render_template('home.html')



if __name__ == "__main__":
    App.run(port=3000)
    

    