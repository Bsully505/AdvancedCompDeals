from flask import Flask,render_template,request
from dotenv import load_dotenv
import json
import requests





# instantiate Slack client
load_dotenv()




App=Flask(__name__)

@App.route('/GetRestResponce',methods=['GET'])
def getResponce():
    headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Mobile Safari/537.36'}
    #req = requests.request(url='https://developer.woot.com/feed/Wootoff?page=1',method='get',headers= headers)
    req = requests.get('https://dealsea.com/search?search_mode=Deals&q=phone',headers= headers)
    return req.text
    
    #this is where we are going to get the request command and then return the json responce 
    


    



@App.route('/')
def index():
    
    return render_template('home.html')



if __name__ == "__main__":
    App.run(port=3000)
    

    