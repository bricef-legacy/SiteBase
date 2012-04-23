import logging

from config import config
from database import users
from sitetools import *
from bottle import request

SECRET = config.get("app", "secret")

logger = logging.getLogger(__name__)


def add_user(username, pwd, perms=[]):
  users.insert({"name":username, "password":pwd, "perms":perms})

def del_user(username):
  user.remove({"name":username})

def get_perms(username):
  return users.find_one({"username":user})["perms"]

def has_perm(user, perm):
  user = users.find_one({"name":user})
  return perm in user.perms

def add_perm(username, perm):
  users.update({"name":username}, {"$push":{"perms":perm}})

def del_perm(username, perm):
  user.update({"name":username}, {"$pull": {"perms":perm}})

def CheckPermission(perm, noauth="noauth"):
  def decorator(function):
    def ifunc(*args, **kwargs):
      username = request.get_cookie("username", secret=SECRET)
      ip = request.environ.get('REMOTE_ADDR')
      if username:
        if has_perm(username, perm):
          return function(*args, **kwargs)
        else:
          print(">>>"+request.path)
          logger.info("'%s' from %s tried to access '%s' without permission."%(username, ip, request.path))
          return renderfile(noauth, {"username":username, "page":request.path})
      else:
        print(">>>"+request.path)
        logger.info("%s tried to access '%s' without logging in"%(ip, request.path))
        return renderfile(noauth, {"page":request.path})
    return ifunc
  return decorator 

