
from bottle import route, run, request, response, get, post 


@route("/")
def home():
  return "Home Sweet Home!"


run(host="0.0.0.0", port="8009", debug=True, reloader=True)
