

import ConfigParser

config = ConfigParser.SafeConfigParser({
  "debug":"False", 
  "templatepath":"./templates/",
  "cache":"False"})

config.read("config.ini")

DEBUG = config.getboolean("app", "debug")
TEMPLATEPATH = config.get("app", "templatepath")
SECRET = config.get("app", "secret")
