from app import app
from app.library.fitur import *
from flask import render_template, request, redirect, jsonify, make_response

# # TODO: -
# # DONE: Udah bisa dapetin response dari flask :D

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == "POST":
      line = request.form["line"]
      print(line)

   return render_template("test.html")

@app.route('/receive-data', methods=['GET', 'POST'])
def receiveData():
   req = request.get_json()
   (message, availID, taskList) = checkFitur(req["line"], req["availID"], req["taskList"])
   res = make_response(jsonify({"message" : message,
                                 "availID" : availID,
                                 "taskList" : taskList}, 200))

   return res