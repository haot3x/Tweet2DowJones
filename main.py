#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# GAE stuff
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

# Twitter stuff
#from TwitterAPI import TwitterAPI,TwitterOAuth


# gae setup
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
)

class Tweet(ndb.Model):
  text = ndb.StringProperty()
  searchTerm = ndb.StringProperty()
  geocode = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

# Twitter setup
# o = TwitterOAuth.read_file() # Using OAuth1...
# api = TwitterAPI(
#                  o.consumer_key,
#                  o.consumer_secret,
#                  o.access_token_key,
#                  o.access_token_secret)

import tweepy
CONSUMER_KEY = '63c0lXM51rxZ2cZUr3QcKKR9q'
CONSUMER_SECRET = 'Kxu44kTkweAkfAVtYVTe2y2Q8FdtkkKFPaMacyihRs1d9eRuU4'
ACCESS_TOKEN_KEY = '37201527-wnO8ILKImZ4SDzTNF3RNTQ9UMZV4oYeBF0t5lA2yU'
ACCESS_TOKEN_SECRET = 'QHkYL3Vk0E1sj4WPPe2EKb1KbEke0SuW3K0Y6Ag4N4GeS'

# api = TwitterAPI(
#     CONSUMER_KEY,
#     CONSUMER_SECRET,
#     ACCESS_TOKEN_KEY,
#     ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class TestHandler(webapp2.RequestHandler):
    def get(self):
        import tweepy
        rst = api.search(q='pizza',geocode='37.781157,-122.398720,1000mi')
        tweets = []
        for t in rst:
            tw = {}
            tw['text'] = t.text
            tw['retweet_count'] = str(t.retweet_count)
            tw['geo'] = str(t.geo)
            tw['lang'] = str(t.lang)
            tweets.append(tw)
        #self.response.write(api.me().name)            
        
        template_values = {
            'tweets':rst
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/test',TestHandler)
], debug=True)
