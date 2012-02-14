

import sys
sys.path.append("./modules/")

import os
import ConfigParser
from functools import *

import pystache
import bottle

from bottle import route, run, request, response, get, post, redirect, abort, static_file, error

#
# Configuration
#
config = ConfigParser.SafeConfigParser()
config.read("config.ini")

bottle.debug(True)

def renderfile(name, data=None):
  #This would be more readable in lisp...Coulda shoulda woulda
  fnames = filter(
                os.path.isfile,
                map(
                  partial(os.path.join, config.get("app", "templatepath")),
                  ["%s.mustache"%name, "%s.html"%name, name]))
  for name in fnames:
    return pystache.render(open(name, "r").read(), data, path=config.get("app", "templatepath"))




def show_flowDiagram():
  return "<h3>flow diagram placeholder</h3>"



pages = {
  "overview" : {
    "name" : "Overview", 
    "href" : "/overview",
    "template" : "overview", 
    "tabs" : [
      { "name" : "Flow Diagram",
        "content" : show_flowDiagram }
    ]
  },
}

def genpage(name):
  if name in pages:
    return renderfile(pages[name]["template"])
  else:
    abort(404, "This page does not exist")


@route("/")
@route("/home")
def home():
  return renderfile("home")

@route("/<name>")
def home(name):
  return genpage(name) 


@route("/static/<filepath:path>")
def static(filepath):
  return static_file(filepath, root="./static/")


@error(404)
def error404(error):
  return renderfile("404")

run(host="0.0.0.0", port="8009", debug=True, reloader=True)
