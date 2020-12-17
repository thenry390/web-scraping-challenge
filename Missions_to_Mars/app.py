from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#code to set up Flask
app = Flask(__name__)

#use flask_pymango to make connection with mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up the Flask routes

# route for the main HTML page 
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("./templates/index.html", mars=mars)

# route for scraping 
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

#run the flask app
if __name__ == "__main__":
    app.run()