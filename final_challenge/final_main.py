"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

title, company, link

Good luck!
"""
from stackoverflow import stack_any_job
from wework import wework_any_job
from remoteok import ok_any_job
from flask import Flask, render_template, request, redirect, send_file
from export import save_to_file


app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = wework_any_job(word)+ok_any_job(word)+stack_any_job(word)
      db[word]=jobs
  else:
    return redirect("/")

  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)

#CSV 저장 활성화

@app.route("/export")
def export():
  try:
    word = request.args.get('word')  
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs,word)
    return send_file(f"{word}.csv",mimetype="text/csv",attachment_filename=f"{word}.csv",as_attachment=True)
  except:
    return redirect("/report")



app.run(host="0.0.0.0")