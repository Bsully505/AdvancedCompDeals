from flask import Flask,render_template,request
from dotenv import load_dotenv
import json
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup




# instantiate Slack client
load_dotenv()




App=Flask(__name__)

#this should be returning a json with the x amount of 
@App.route('/GetRestResponse',methods=['GET'])
def getResponse():
    query = request.args.get('keyWord')
    Time = request.args.get('time')
    callResponse = CallAPI(query,10)
    res = ParseHTML(callResponse)
    #parse req.text and then send back 
    return res
    
    #this is where we are going to get the request command and then return the json responce 
    

#Henoks part is to parse using req test and be able to send it to front end 
def ParseHTML(str):
    # use this library to parse out the desired items HTMLParser 
    # and then return the html 
    printDeals(str)
    
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


def printDeals(res):
    prinres = {}
    res2 = BeautifulSoup(res.text,'html.parser')
    val = BeautifulSoup((res2.find(id='fp-deals').text),'html.parser').contents[0].split('\n\n')
    val = val[2:]
    for vaz in val: 
        if(vaz.split(' ')[0]!='(Expired)'):
            prinres+=vaz.split('\n')[0]
            print(prinres)
    return prinres
            
            
def GetNextURL(res):
    res2 = BeautifulSoup(res.text,'html.parser')
    res3 = res2.find_all('a')
    #find all('a') on 12 index is the next parameter 
    if('Next' in res3[12]):
        NextURL = res3[12]['href']            
        return (NextURL)
    
def CallNextPage(query):
    headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36'}
    req = requests.get(f'https://dealsea.com/search?{query}',headers= headers)
    return req

def postOntoJson(res):
    pass
    #input into json a list 

    



@App.route('/')
def index():
    
    return render_template('home.html')



if __name__ == "__main__":
    App.run(port=3000)
    

    