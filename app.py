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
from config import config



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
def home():
  return renderfile("root", {})


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

