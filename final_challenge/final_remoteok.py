import requests
from bs4 import BeautifulSoup

def ok_any_job(word):
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  results = requests.get(url, headers=headers)
  soup = BeautifulSoup(results.text,"html.parser")
  ok_data = soup.find_all("tr",{"class":"remoteok-original"})
  jobs=[]
  for data in ok_data:
    title = data.select_one("td.company_and_position_mobile > a.preventLink > h2").string
    company = data["data-company"]
    link = data["data-url"]
    info = {'title':title,'company':company,'link':"https://remoteok.io"+link}
    jobs.append(info)
  return jobs