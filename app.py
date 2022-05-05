
from flask import Flask,render_template,request
import json
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup



App=Flask(__name__)


@App.route('/GetRestResponse',methods=['POST'])
def getResponse():
    postRes = request.get_json()
    query = postRes['Query']
    Time = postRes['Time']
    PostQuery(query)
    PostTime(Time)
    callResponse = CallAPI(query,0)
    res = ParseHTML(callResponse)
    SetDealMethod(res)
    #parse req.text and then send back 
    return "Success"
    
    
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


def PostQuery(inserter):
    #inserter = request.get_json['Query']
    
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    text[0]['Query']= inserter
    json.dump(text,FileEditer,indent=3)
    FileEditer.close()
    return "Success"



def PostTime(inserter):
    #inserter = request.get_json['Time']
    
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    text[0]['Time']= inserter
    json.dump(text,FileEditer,indent=3)
    FileEditer.close()
    return "Success"


@App.route('/SetDeal',methods=['POST'])
def SetDeal():
    deals = request.get_json['Deals']
    #deals = request.args.get('Deals')
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    #if working with request args
    #text[1]=[{"deal":deals}]
    #if working with getJson
    text[1] = deals
    json.dump(text, FileEditer,indent=3)
    FileEditer.close()
    return "Successfully Set Deal"


def SetDealMethod(lis):

    FileOpener = open('data.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    ret=[]
    for val in lis:
        ret.append({"Deals":val})
    if(len(lis)==0):
        ret.append({"Deals":"No deals were found"})
    text[1] = ret
    json.dump(text, FileEditer,indent=3)
    FileEditer.close()
    return "Successfully Set Deal"




@App.route('/AppendDeal',methods=['GET'])
def AppendDeal():
    #deals = request.get_json['Deals']
    deals = request.args.get('Deals')
    FileOpener = open('data.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    json.dump(text, FileEditer,indent=3)
    FileEditer.close()
    return "Successfully Reset to default"
    

@App.route('/SetTemplate',methods=['GET'])
def Template():
    FileOpener = open('Template.json')
    text = json.load(FileOpener)
    FileOpener.close()
    FileEditer = open('data.json','w')
    json.dump(text, FileEditer,indent=3)
    FileEditer.close()
    return "Successfully Reset to default"
    


    #this is where we are going to get the request command and then return the json responce 
    

#Henoks part is to parse using req test and be able to send it to front end 
def ParseHTML(str):
    # use this library to parse out the desired items HTMLParser 
    # and then return the html 
    str = printDeals(str)
    
    return str

        
        
def CallAPI(query, startIndex):
    headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36'}
    req = requests.get(f'https://dealsea.com/search?search_mode=Deals&q={query}&n={startIndex}',headers= headers)
    return req


def printDeals(res):
    prinres = []
    i= 0
    url = "test"
    res4= res
    while(i<5 and len(prinres)<10 and url):
        res2 = BeautifulSoup(res4.text,'html.parser')
        val = res2.find(id='fp-deals').text.split("\n\n")
        val = val[2:]
        for vaz in val: 
            if(vaz.split(' ')[0]!='(Expired)' and len(prinres)<10):
                prinres.append(vaz.split('\n')[0])
        i=i+1
        url = GetNextURL(res4)
        #this is happening when it shouldnt be 
        if(url is None):
            print("short circuit")
            return prinres
        print(url)
        res4= CallNextPage(url)
    return prinres
      
def GetNextURL(res):
            
    res2 = BeautifulSoup(res.text,'html.parser')
    res3 = res2.find_all('a')
    #find all('a') on 12 index is the next parameter 
    if('Next' in res3[12]):
        NextURL = res3[12]['href']            
        return (NextURL)
    #this happens if not in the 
    if('Next' in res3[13]):
        NextURL = res3[13]['href'] 
        return (NextURL)
    return None
    
def CallNextPage(query):
    headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36'}
    req = requests.get(f'https://dealsea.com/{query}',headers= headers)
    return req




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






if __name__ == "__main__":
    App.run(port=3000)
    

    