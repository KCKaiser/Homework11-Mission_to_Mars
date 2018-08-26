from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape

###########################################################################

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

###########################################################################

doc = scrape()

db = client.homework_11_db

db.mission_to_mars.drop()

db.mission_to_mars.insert(doc)


###########################################################################

app = Flask(__name__)

@app.route("/")
def index():
    document = db.mission_to_mars.find()[0]
    return render_template('index.html', dict = document)

@app.route("/scrape")
def scraped():
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    
    doc = scrape()
    db = client.homework_11_db
    db.mission_to_mars.drop()
    db.mission_to_mars.insert(doc)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False)
