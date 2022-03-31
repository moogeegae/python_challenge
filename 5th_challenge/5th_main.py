import os
import requests
from bs4 import BeautifulSoup

#extracted_function
def extract_data(i,k):
  url = "http://www.iban.com/currency-codes"
  iban_result=requests.get(url)
  iban_soup=BeautifulSoup(iban_result.text,"html.parser")
  table_raw = iban_soup.find("table", {"class":"table-bordered"})
  a=[]
  words=table_raw.select(f"tbody > tr > td:nth-child({i})")
  for word in words:
    word=word.text
    if (word=="" or word=="No universal currency") and k==1:
      continue
    a.append(word)
  return a

def extract_name():
  name=extract_data(1,2)
  currency=extract_data(2,2)
  a = [i for i, value in enumerate(currency) if value == "No universal currency"]
  new_name=[]
  j=0
  for j in range(268):
    if j in a:
      continue
    else:
      new_name.append(name[j])
  return new_name

def page_print():
  for idx, val in enumerate(name):
    print(f"# {idx} {val}")

def main():
  try:
    input_word=int(input("#:"))
    if input_word <264:
      print(f"You chose {name[input_word]}")
      print(f"The currency code is {code[input_word]}")
      return
    else:
      print("Choose a number from the list.")
      main()
  except:
    print("That wasn't a number")
    main()

#execute
os.system("clear")
name=extract_name()
code=extract_data(3,1)
print("Hello! Please choose select a country by number:")
page_print()
main()