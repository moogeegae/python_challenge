import requests

#create type - http;//url
def http(url):
  if "http" in url or "http://" in url:
    return url
  else:
    return "http://" + url

print("Welcome to IsItDown.py!")

while True:
  url_raw=input("Please write a URL or URLs you want to check. (separated by comma)\n").strip().split(",")

  urlgroup=[]
  for url_baby in url_raw:
    urlgroup = urlgroup + [url_baby.strip()]
    
  for url in urlgroup:
    if ".com" not in url:
      print(f"{url} is not a valid URL.")
    else:
      try:
        url_format=http(url)
        urls = requests.get(url_format)
        if urls.status_code ==200:
          print(f"{url_format} is up!")
        else:
          print(f"{url_format} is down!") 
      except:
        print(f"{url_format} is down!")

  while True:
    gogoagain=input("Do you want to start over? y/n\t")
    if gogoagain == "y" or gogoagain == "n":
      break    
    else:
      print("That's not a valid answer")

  if gogoagain =="n":
    print("ok, bye!")
    break
  else:
    continue

