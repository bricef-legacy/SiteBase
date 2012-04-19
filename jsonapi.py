import os
import sys
mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,mypath)
sys.path.insert(0,os.path.join(mypath, "modules"))
os.chdir(mypath)

#stdlib modules
import json
import time

# third party modules
from bottle import *

# my modules
from config import config
from database import books
from sitetools import *
import users

app = Bottle()

def document(func):
  func.document = True
  return func

#
# API Functions
# 
@app.route("/books")
@users.CheckPermission("READ")
def json_books():
  response.set_header('Content-type', 'application/json')
  return json.dumps(books.find())


#
# Automagic utilities
#
@document
@app.route('/status')
def api_status():
  """returns the server status and server time."""
  return {'status':'online', 'servertime':time.time()}

@app.route('/docs')
def autodoc():
  #the idea is to extract the route information out of the functions
  return {"functions":  [ {"route": None, "doc":v.__doc__} for k,v in globals().items() if hasattr(v, "document") and v.document == True]}

@app.error(500)
def error(error):
  response.set_header("Content-Type", "application/json")
  return json.dumps({"error": str(error.output)})
