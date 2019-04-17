from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import json
from bson import json_util


# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/dog_meme_db"

mongo = PyMongo(app)

db = mongo.db
collection = db.dog_meme_predictions

#create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    cursor = list(collection.find())
    # return template and data
    return render_template("index.html", dog_meme_dict=cursor)


@app.route("/dog_list")
def dog_list():

    #convert collection into a dictionary for the json dumps function
    dog_list_dict = list(collection.find())

    #return json data when the route is called
    return json.dumps(dog_list_dict, default=json_util.default)
    


if __name__ == "__main__":
    app.run(debug=True)
