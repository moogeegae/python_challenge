import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

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

os.system("clear")
name=extract_name()
code=extract_data(3,1)
print("Welcome to currencyConvert PRO 2000\n")
for idx, val in enumerate(name):
  print(f"# {idx} {val}")

#execute
def main():
  try:
    while True:
      print("\nWhere are you from? Choose a country by number.\n")
      first_country=int(input("#:"))
      print(name[first_country])
      print("\nNow choose another country.\n")
      second_country=int(input("#:"))
      print(name[second_country])
      input_word=input(f"\nHow many {name[first_country]} do you want to convert to {name[second_country]}?\n")
      if input_word.isdigit() == True:
        break
      else:
        print("That wasn't a number.")

    convert_result = requests.get(f"https://www.transferwise.com/gb/currency-converter/{code[first_country]}-to-{code[second_country]}-rate")

    convert_soup = BeautifulSoup(convert_result.text,"html.parser")
    convert_span = convert_soup.find("h3",{"class":"cc__source-to-target"}).find_all('span')[2].text

    in_number=float(input_word)
    convert_constant = float(convert_span)

    money1_unit = format_currency(in_number,code[first_country],format=u'¤#,##0.00',locale="ko_KR")
    money2_unit = format_currency(in_number*convert_constant,code[second_country],format=u'¤#,##0.00',locale="ko_KR")
    print(f"{money1_unit} is {money2_unit}")
  except:
    print("This country has not currency in Transfer Wise. Please choose another country")
    main()

main()