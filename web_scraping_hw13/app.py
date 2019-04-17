from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars"
mongo = PyMongo(app)


# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")

#create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_data_mongo = mongo.db.collection.find()

    

    # return template and data
    return render_template("index.html", mars_data_dict = mars_data_mongo)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    #scrape_weather() is the function built in the other python file (scrape_info.py)
    mars_data = scrape_mars.mars_scrape_function()

    # # Store results into a dictionary
    mars_dict = { "headlines" : mars_data["mars_news_headline"],
                "paragraphs" : mars_data["mars_news_par"],
                "feature_images" : mars_data["mars_feature_images"],
                "weather" : mars_data["mars_weather"],
                "facts" : mars_data["mars_facts"],
                "hemisphere_images" : mars_data["mars_hemisphere_images"]
            }
    
    # Insert forecast into database
    mongo.db.collection.insert_one(mars_dict)

    return redirect("/", code=302)
    

if __name__ == "__main__":
    app.run(debug=True)

