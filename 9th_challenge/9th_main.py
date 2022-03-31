import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")
@app.route("/")
def home():
  return render_template('home.html',subreddits=subreddits)

@app.route("/read")
def read():
  name = list(request.args.to_dict().keys())
  def make_list(kind):
    kind_list=[]
    for element in kind[:6]:
      if kind == 'upvotes':
        element=int(element.text)
      else:
         element=element.text
      kind_list.append(element)
    return kind_list

  def make_link(kind):
    links=[]
    for lin in kind:
      links.append(lin.get('href'))
    return links

  def make_dict(subreddit):
    if subreddit == "reactjs":
      url="https://www.reddit.com/r/reactjs/top/?t=month"
      results=requests.get(url,headers=headers)
      soup=BeautifulSoup(results.text,"html.parser")
      upvotes=soup.select("div._1rZYMD_4xY3gRcSS3p8ODO._25IkBM0rRUqWX5ZojEMAFQ")
      links=soup.select("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")
      titles=soup.select("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE > div._2SdHzo12ISmrC8H86TgSCp > h3._eYtD2XCVieq6emjKBH3m")
    else:
      url=f"http://www.reddit.com/r/{subreddit}/top/?t=month"
      results=requests.get(url,headers=headers)
      soup=BeautifulSoup(results.text,"html.parser")
      upvotes=soup.select("div._3xuFbFM3vrCqdGuKGhhhn0 > div._23h0-EcaBUorIHC-JZyh6J > div._1E9mcoVn4MYnuBQSVDt1gC > div._1rZYMD_4xY3gRcSS3p8ODO")
      links=soup.select("div._3xuFbFM3vrCqdGuKGhhhn0 > div._1poyrkZ7g36PawDueRza-J > article.yn9v_hQEhjlRNZI0xspbA > div._32pB7ODBwG3OSx1u_17g58 > div._2FCtq-QzlfuN-SwVMUZMM3 > div.y8HYJ-y_lTUHkQIc1mdCq > a")    
      titles=soup.select("div._3xuFbFM3vrCqdGuKGhhhn0 > div._1poyrkZ7g36PawDueRza-J > article.yn9v_hQEhjlRNZI0xspbA > div._32pB7ODBwG3OSx1u_17g58 > div._2FCtq-QzlfuN-SwVMUZMM3 > div.y8HYJ-y_lTUHkQIc1mdCq > a.SQnoC3ObvgnGjWt90zD9Z > div._2SdHzo12ISmrC8H86TgSCp > h3._eYtD2XCVieq6emjKBH3m")

    vote=make_list(upvotes)
    link=make_link(links)
    title=make_list(titles)
    data=[]
    for i in range(len(vote)):
      info = {'vote':vote[i],'link':link[i],'title':title[i],'subreddit':subreddit}
      data.append(info)
    return data
    
  def list_data():
    final_data=[]
    for nm in name:
      final_data = final_data + make_dict(nm)  
    return final_data
  
  return render_template('read.html',name=name,final_data=list_data())

app.run(host="0.0.0.0")