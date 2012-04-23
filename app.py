#!/usr/bin/env python

import sys
import os
mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,mypath)
sys.path.insert(0,os.path.join(mypath, "modules"))
os.chdir(mypath)import os

# Standard lib modules
import argparse

# Third party modules
import bottle
from bottle import route, run, request, response, get, post, redirect, abort, static_file, error, mount

# My modules
from sitetools import *
from config import config, SECRET
import users



#########################
#
# Configuration
#
#########################

bottle.debug(True)

###############################
#
# Route Handlers 
#
###############################

@route("/")
@route("/home")
def home():
  return renderfile("home", {})

@app.route("/register")
@app.get("/register")
@app.post("/register")
def register():
  username = request.forms.get("username")
  password = request.forms.get("password")
  password2 = request.forms.get("password2")
  data = {"username":username, 
          "messages":[],
          "warnings": []} 
  
  if password == password2 and username:
    try:
      users.add_user(username, password)
    except UserNameExistsException as ex:
      data["warnings"].append("This username is already taken")
      return renderfile("register", data)
    return login()
  elif not username:
    data["warnings"].append( "You can't have an empty name")
  elif password != password2:
    data["warnings"].append( "Your two passwords don't match")
  return renderfile("register", data)

@route('/login')
@get('/login')
@post('/login')
def login():
  username = request.get_cookie("account", secret=SECRET)
  if not username:
    username = request.forms.get('username')
    password = request.forms.get('password')
    if users.auth_ok(username, password):
        response.set_cookie("account", username, secret=SECRET)
        redirect("/home") 
    else:
      return renderfile("login", {"warnings":[{"msg":"Wrong username or password."}]})
  else:
    redirect("/")

@route('/logout')
def logout():
    response.delete_cookie("account")
    redirect("/")

@route("/fail/<report>/<graph>")
def show_fragment(report, graph):
  abort(404, "This page does not exist") 

@route("/static/<filepath:path>")
def static(filepath):
  return static_file(filepath, root="./static/")


###############################
#
# Mount API on /api/ 
#
###############################
from jsonapi import app as api_app
mount("/api/", api_app)


###############################
#
# Handle Errors 
#
###############################
@error(404)
def error404(error):
  return renderfile("404")


#
# Main. To run in developer mode simply pass --run
# 
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run appliation')
  parser.add_argument(
    "--run",
    action='store_true',
    help='Run the webapp in developer mode'
  )
  args = parser.parse_args()

  if args.run:
    run(host="0.0.0.0", port="8009", debug=True, reloader=True)

else:
  application = bottle.default_app()

