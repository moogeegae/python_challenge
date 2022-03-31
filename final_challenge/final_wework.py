import requests
from bs4 import BeautifulSoup

def wework_any_job(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  results = requests.get(url)
  soup = BeautifulSoup(results.text,"html.parser")
  wework_data = soup.select("div.jobs-container > section > article > ul > li")
  jobs=[]
  for data in wework_data[:-1]:
    title = data.find("span",{"class":"title"})
    company = data.find("span",{"class":"company"})
    if title==None or company==None:
      pass
    else:
      title_1 = title.string
      company_1 = company.string
    link = data.find("a")["href"]
    info = {'title':title_1,'company':company_1,'link':"https://weworkremotely.com"+link}
    jobs.append(info)
  return jobs