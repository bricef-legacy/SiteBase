

import ConfigParser

config = ConfigParser.SafeConfigParser({
  "debug":"False", 
  "production":"True", 
  "templatepath":"./templates/",
  "cache":"False"})

config.read("config.ini")

DEBUG = config.getboolean("app", "debug")
PRODUCTION = config.getboolean("app", "production")
TEMPLATEPATH = config.get("app", "templatepath")

