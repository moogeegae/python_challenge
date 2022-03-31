import os
import csv
import requests
from bs4 import BeautifulSoup
#url, company name(csv filename)
os.system('clear')
alba_url = "http://www.alba.co.kr"
alba_result = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_result.text, "html.parser")
logo = alba_soup.find("div", {"id": "MainSuperBrand"})
logo_company = logo.select("ul > li > a.goodsBox-info > span:nth-child(2)")
logo_url = logo.select("ul > li > a.goodsBox-info")
company = []
urls = []
for data in logo_company:
    company.append(data.text)
for url_data in logo_url:
    if url_data['href'] not in urls:
        urls.append(url_data['href'])
#last page by company
def extract_alba_pages(url):
    html = requests.get(f"{url}?page&pagesize=50")
    soup = BeautifulSoup(html.text, 'html.parser')
    num = soup.select("div#NormalInfo > p > strong")
    page = 0
    alba_num = int(num[0].text.strip().replace(',', ''))
    while True:
        try:
            page = page + 1            
            if alba_num/50 <= 1:
                raise NotImplementedError
            else:
              alba_num=alba_num-50
        except:
            break
    return page
#extract date
def extract_alba_jobs(last_page):
  info_job = []
  for page in range(last_page):
    print(page+1)
    result = requests.get(f"{url}?page={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.select("div.goodsList.goodsJob > table > tbody > tr")
    for rslt in results:
      place = rslt.select_one('td.local.first')
      title = rslt.select_one('td.title > a > span.company')
      work_time = rslt.select_one('td.data > span.time')
      pay = rslt.select_one('td.pay')
      up_date = rslt.select_one('td.regDate.last')
      if place != None and work_time != None and title != None and pay != None and up_date != None:
        info = {
          'place': place.text,
          'title': title.text,
          'work_time': work_time.text,
          'pay': pay.text,
          'up_date': up_date.text
          }
        info_job.append(info)
  return info_job
#Connect a function so that it is not messy
def get_jobs(url):
  last_alba_page=extract_alba_pages(url)
  alba_jobs=extract_alba_jobs(last_alba_page)
  return alba_jobs
#csv file -  saving function
def save_to_file(jobs,i):
  file = open(f"{company[i]}.csv".replace("/",","), mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "work_time", "pay", "up_date"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return []

"""

-------------------------------------------------------------------------------------
It takes a long time to execute.
I printed out the address and company name to indicate which company we are currently web-scrapping.
You can find out the progress by printing out which page you are currently scrap.
-------------------------------------------------------------------------------------

"""

#execute (save csv files)
for i in range(len(urls)):
  url = urls[i]
  print(urls[i],company[i],f"execute_number_{i+1}")
  save_to_file(get_jobs(url),i)

