
try:
  import configparser 
except ImportError:
  import ConfigParser as configparser

config = configparser.SafeConfigParser({
  "debug":"False", 
  "templatepath":"./templates/",
  "cache":"False"})

config.read("config.ini")

DEBUG = config.getboolean("app", "debug")
CACHE = config.getboolean("app", "cache")
TEMPLATEPATH = config.get("app", "templatepath")
SECRET = config.get("app", "secret")
