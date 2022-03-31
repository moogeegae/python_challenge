import requests
from flask import Flask, render_template, request



base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

popular_data = requests.get(popular).json()["hits"]
new_data = requests.get(new).json()["hits"]

app = Flask("DayNine")
db = {}

def fakeDB(data):
  fake_db=[]
  for in_data in data:
    objectID = in_data['objectID']
    title = in_data['title']
    url = in_data['url']
    points = in_data['points']
    author = in_data['author']
    num_comments = in_data['num_comments']
    extracted_data = {'objectID':objectID,'title':title,'url':url,'points':points,'author':author,'num_comments':num_comments}
    if extracted_data in fake_db:
      pass
    else:
      fake_db.append(extracted_data)
  if data == new_data:
    db['new']=fake_db
  else:
    db['popular']=fake_db

def hi_data(request):
  fakeDB(new_data)
  fakeDB(popular_data)  
  order_by = request.args.get("order_by")
  if order_by == 'new':
    return render_template("index.html",dict_data=db['new'],order_by='new')
  elif order_by == 'popular':
    return render_template("index.html",dict_data=db['popular'],order_by='popular')
  else:
    return render_template("index.html",dict_data=db['popular'],order_by='popular')
'----------------------------------------------------------------------------'
@app.route("/")
def home():
  return hi_data(request)

@app.route("/?order_by=new")
def new():
  return hi_data(request)

@app.route("/?order_by=popular")
def popular():
  return hi_data(request)

@app.route("/<id>")
def detail(id):
  id_data = requests.get(make_detail_url(id)).json()
  return render_template("detail.html",dict_data = id_data['children'],head_data=id_data)

app.run(host="0.0.0.0")
