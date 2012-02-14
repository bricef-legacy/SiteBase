

import sys
sys.path.append("./modules/")

import pystache
import bottle

from bottle import route, run, request, response, get, post, redirect, abort


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
                  ["%S.mustache"%name, "%s.html"%name, name]))
  for name in fnames:
    return pystache.render(open(name, "r").read, data, path=config.get("app", "templatepath"))

@route("/")
def home():
  return "Home Sweet Home!"


run(host="0.0.0.0", port="8009", debug=True, reloader=True)
