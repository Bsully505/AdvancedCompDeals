from flask import Flask,render_template,request
from dotenv import load_dotenv
import json
from Conversion import Conversion





# instantiate Slack client
load_dotenv()



App=Flask(__name__)



    



@App.route('/')
def index():
    
    return render_template('home.html')



if __name__ == "__main__":
    KeyURL = Conversion()
    App.run(port=3000)
    

    