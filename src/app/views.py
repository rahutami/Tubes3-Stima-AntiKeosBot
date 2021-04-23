from app import app
from app.library.fitur import *
from flask import render_template, request, redirect, jsonify, make_response

# # TODO: Kirim message dari server ke browser
# # DONE: Udah bisa dapetin message dan data dari local storage

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == "POST":
      line = request.form["line"]
      print(line)

   return render_template("test.html")

@app.route('/receive-data', methods=['GET', 'POST'])
def receiveData():
   req = request.get_json()
   print(req)
   res = make_response(jsonify({"message" : "thanks"}, 200))

   return res

@app.route('/about')
def about():
   return "Hey this is about"

@app.route('/signup', methods=['GET', 'POST'])
def method_name():
   if request.method == "POST":
      line = request.form["line"]
      print(line)

   return render_template("test.html")