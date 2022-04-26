from flask import Flask,render_template,request
from dotenv import load_dotenv
import json
import requests





# instantiate Slack client
load_dotenv()




App=Flask(__name__)

@App.route('/GetRestResponce',methods=['POST'])
def getResponce():
    pass
    #this is where we are going to get the request command and then return the json responce 
    


    



@App.route('/')
def index():
    
    return render_template('home.html')



if __name__ == "__main__":
    App.run(port=3000)
    

    