import requests
from bs4 import BeautifulSoup

def stack_page(url):
  results = requests.get(url)
  soup = BeautifulSoup(results.text,"html.parser")
  page = soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page = page[-2].text.strip()
  return last_page

def extracted_job(last_page,url):
  jobs=[]
  for page in range(int(last_page)):
    results = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(results.text,"html.parser")
    stack_data = soup.find_all("div", {"class": "-job"})
    for data in stack_data:
      title = data.find("h2",{"class":"mb4"}).find("a")["title"]
      company = data.select("h3.mb4 > span:nth-child(1)")[0].text.replace("\r\n","").strip()
      link = data.find("h2",{"class":"mb4"}).find("a")["href"]
      info = {'title':title,'company':company,'link':"https://stackoverflow.com"+link}
      jobs.append(info)
  return jobs

def stack_any_job(word):
  url = f"https://stackoverflow.com/jobs?r=true&q={word}"
  last_page = stack_page(url)
  result = extracted_job(last_page,url)
  return result