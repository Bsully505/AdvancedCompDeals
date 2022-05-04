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
@App.route('/GetRestResponseOld',methods=['GET'])
def getResponseOld():
    query = request.args.get('keyWord')
    Time = request.args.get('time')
    callResponse = CallAPI(query,0)
    res = ParseHTML(callResponse)
    #parse req.text and then send back 
    return res

@App.route('/GetRestResponse',methods=['POST'])
def getResponse():
    postRes = request.get_json()
    query = postRes['query']
    Time = postRes['time']
    callResponse = CallAPI(query,0)
    res = ParseHTML(callResponse)
    #parse req.text and then send back 
    return res
    
    
@App.route('/GetQuery')
def GetDataFromFile1():
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    return str(text[0]['Query'])



@App.route('/GetTime')
def GetDataFromFile2():
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    return str(text[0]['Time'])


    #this is where we are going to get the request command and then return the json responce 
    

#Henoks part is to parse using req test and be able to send it to front end 
def ParseHTML(str):
    # use this library to parse out the desired items HTMLParser 
    # and then return the html 
    str = printDeals(str)
    
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
    prinres = []
    res2 = BeautifulSoup(res.text,'html.parser')
    val = res2.find(id='fp-deals').text.split("\n\n")
    val = val[2:]
    for vaz in val: 
        if(vaz.split(' ')[0]!='(Expired)'):
            prinres.append(vaz.split('\n')[0])
    json_String = json.dumps(prinres)
    return json_String
      
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


@App.route('/data')
def GetData():
    val =open("data.json")
    jInter = json.load(val)
    val.close()
    return json.dumps(jInter)


def editJson(deals):
    val = open("data.json")
    jInter = json.load(val)
    val.close()
    openval = open("data.json","w")
    lis=[]
    for i in deals:
        lis.append({"deal": i})
    jInter[1] = lis
    json.dump(jInter,openval,indent=3)
    openval.close()
    return True

@App.route('/')
def index():
    
    return render_template('home.html')


@App.route('/s')
def indexs():
    
    return render_template('home.html')



if __name__ == "__main__":
    App.run(port=3000)
    

    