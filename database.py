#!/usr/bin/env python
from functools import *

import pymongo

from sitetools import *
from config import config

conn = pymongo.Connection("localhost", 27017)
db = conn.bookdb
db.users.ensure_index("name")
users = db.users
books = db.books

