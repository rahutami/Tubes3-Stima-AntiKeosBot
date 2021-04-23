from app import app
from app import fitur
from flask import render_template, request, redirect

# # TODO: Dapetin data dari local storage
# # DONE: Udah bisa dapetin message dari input

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == "POST":
      req = request.form
      print(req)
      return redirect(request.url)

   return render_template("index.html")

@app.route('/about')
def about():
   return "Hey this is about"

@app.route('/signup', methods=['GET', 'POST'])
def method_name():
   if request.method == "POST":
      line = request.form.to_dict()["line"]
      print(line)

   return render_template("test.html")