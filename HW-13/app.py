from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from scraper import scraped


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mars'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars'
mongo = PyMongo(app)

@app.route("/")
def index():
    obj = mongo.db.mars.find_one(
        sort=[('_id',-1)]
)
    return render_template("home.html", obj=obj)
	
@app.route("/scrape")
def insert_and_redirect():
    for_insert = scraped()
    mongo.db.mars.insert_one(for_insert)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=8111,debug=True)