"""Import and run app."""
#from aimechanic_app import create_app

#app = create_app()

#if __name__ == "__main__":
#    app.run(debug=True)

#"""Import and run app."""
#from aimechanic_app import app

#if __name__ == "__main__":
#    app.run(debug=True)

from flask import Flask, request, redirect, render_template, url_for
#from flask_pymongo import PyMongo
from bson.objectid import ObjectId
#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
from main import askQuestion

from datetime import datetime
import calendar
import os
from dotenv import load_dotenv

# Written with help from https://www.guru99.com/calendar-in-python.html

############################################################
# SETUP
############################################################



############################################################
# ROUTES
############################################################

def create_app():

    app = Flask(__name__)
    load_dotenv()
    
# Send a ping to confirm a successful connection

    @app.route('/', methods=['GET', 'POST'])
    def base():
        """Display the events list page."""

        if request.method == 'POST':
            prompt = request.form.get('prompt')
            outputPresent=True

            output=askQuestion(prompt)
            return render_template('base.html', output=output, outputPresent=outputPresent)
        else:
            outputPresent=False
  
        return render_template('base.html', outputPresent=outputPresent)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
