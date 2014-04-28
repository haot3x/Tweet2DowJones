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
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
)

GEO_LIST = [
            ["LA","34.002854,-118.110295,100mi"],
            ["NYC","40.767024,-73.973884,100mi"],
            ["CHI","41.849591,-87.690270,100mi"],
            ["ATL","33.759293,-84.387817,100mi"]
            ]
Q_TERMS = ["i feel","i am feeling","i'm feeling","i dont feel","i'm","Im","I am","makes me"]
GEO_DICT = dict(zip(map(lambda x: x[0], GEO_LIST),map(lambda x: x[1], GEO_LIST)))




class Tweet(ndb.Model):
    searchTerm = ndb.StringProperty()
    searchGeo = ndb.StringProperty()
    searchGeoPlace = ndb.StringProperty()
    processed = ndb.BooleanProperty(default=False)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    id = ndb.IntegerProperty()
    text = ndb.StringProperty()
    created_at = ndb.DateTimeProperty()
    geo = ndb.StringProperty()
    favorite_count = ndb.IntegerProperty()
    retweet_count = ndb.IntegerProperty()

class DJI(ndb.Model):
    dji = ndb.FloatProperty()    
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


import tweepy
CONSUMER_KEY = '63c0lXM51rxZ2cZUr3QcKKR9q'
CONSUMER_SECRET = 'Kxu44kTkweAkfAVtYVTe2y2Q8FdtkkKFPaMacyihRs1d9eRuU4'
ACCESS_TOKEN_KEY = '37201527-wnO8ILKImZ4SDzTNF3RNTQ9UMZV4oYeBF0t5lA2yU'
ACCESS_TOKEN_SECRET = 'QHkYL3Vk0E1sj4WPPe2EKb1KbEke0SuW3K0Y6Ag4N4GeS'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)




##########################################################################
def json_date_handler(obj):
#    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
    import datetime
    return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj,datetime.datetime) else obj


class NDBStatsHandler(webapp2.RequestHandler):
    def get(self):
        stats = []
        for q in Q_TERMS: 
            cnt = Tweet.query(Tweet.searchTerm==q).count()
            stats.append({"q":q,"cnt":cnt})
        stats.append({"q":"TOTAL","cnt":Tweet.query().count()})
        


        template_values = {
             'arr':stats,
             'dji_cnt':DJI.query().count()
        }
        template = JINJA_ENVIRONMENT.get_template('ndb_stats.html')
        self.response.out.write(template.render(template_values))

class CronDummyHandler(webapp2.RequestHandler):
    def get(self):
        pass

class CronFetchTweetHandler(webapp2.RequestHandler):
    def get(self):
        cnt = 0
        for city in GEO_LIST:
            for q in Q_TERMS:
                cnt += self.__get_tweet(q=q,geocode=city[1])
        logging.info('CRON cron_fetch_tweet DONE - %d tweets'%(cnt,))
        #self.response.out.write(str(cnt))

    def __get_tweet(self,q='pizza',geocode="40.767024,-73.973884,100mi"):
        
        if Tweet.query(Tweet.searchTerm==q).count() > 0:
            since_id = Tweet.query(Tweet.searchTerm==q).order(-Tweet.id).fetch(1)[0].id
        else:
            since_id = 0

        logging.info('__get_tweet: q=%s,geocode=%s,since_id=%d' % (q,geocode,since_id))

        rst = api.search(q=q,geocode=geocode,since_id=since_id,count=100)
        
        tws = []
        for t in rst:
            tweet = Tweet(  searchTerm = q,
                            searchGeo = geocode,
                            id = t.id,
                            text = t.text,
                            created_at = t.created_at,
                            geo = str(t.geo),
                            favorite_count = t.favorite_count,
                            retweet_count = t.retweet_count
                            )
            #tweet.put()
            tws.append(tweet)
        ndb.put_multi(tws)
        return len(rst)
        

class CronFetchDJIHandler(webapp2.RequestHandler):
    def get(self):
        from HTMLParser import HTMLParser
        class DJIHTMLParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.found = False
                self.dji = 0
            def handle_starttag(self, tag, attrs):
                for a in attrs:
                    if a[0] == 'id' and a[1] == 'yfs_l10_^dji':
                        #print "n %s v %s" % (a[0],a[1])
                        self.found = True
            def handle_data(self, data):
                if self.found is True:
                    #print "Encountered some data  :", data
                    self.dji = data
                    self.found = False

        baseurl = "http://finance.yahoo.com/q/bc?s=%5EDJI+Basic+Chart"
        htmlcontent = "".join(urllib.urlopen(baseurl))
        parser = DJIHTMLParser()
        parser.feed(htmlcontent)
        dji_price = float(parser.dji.replace(',',''))        
        dj = DJI(dji = dji_price)
        dj.put()
        print dji_price
        self.response.out.write(dji_price)

class NDBDeleteHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        keys = Tweet.query(Tweet.searchTerm==q).fetch(keys_only=True)
        # toDel = ndb.get_multi(keys)
        # for d in toDel:
        #     print d.created_at
        ndb.delete_multi(keys)
        self.response.write(len(keys))

class NDBDeleteAllHandler(webapp2.RequestHandler):
    def get(self):

        cnt1 = Tweet.query().count()
        cnt2 = DJI.query().count()
        
        errorMsg = ""

        while Tweet.query().count()>0 or DJI.query().count()>0: 
            try:
                while Tweet.query().count() > 0:
                    keys = Tweet.query().fetch(2000,keys_only=True)
                    ndb.delete_multi(keys)
                
                while DJI.query().count() > 0:
                    keys = DJI.query().fetch(2000,keys_only=True)
                    ndb.delete_multi(keys)
            except Exception, e: #DeadlineExceededErrors
                errorMsg = errorMsg + str(e)

        msg = "deleted: %d Tweet objects, %d DJI objects." % (cnt1,cnt2)
        self.response.write(msg + "</br></br></br>" + errorMsg)

class DJIJsonHandler(webapp2.RequestHandler):    
    def get(self):
        import json
        jd = json.dumps([t.to_dict() for t in DJI.query().order(DJI.timestamp).fetch()],default=json_date_handler)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(jd)


class TweetJsonDumpHandler(webapp2.RequestHandler):
    
    def get(self):
        import json
        q = self.request.get('q')
        if q is '':
            jd = json.dumps([t.to_dict() for t in Tweet.query().fetch()],default=json_date_handler)
            print "all"
        else:
            jd = json.dumps([t.to_dict() for t in Tweet.query(Tweet.searchTerm == q).fetch()],default=json_date_handler)
            print q
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(jd)

class TweetJsonDownloadHandler(webapp2.RequestHandler):
    def get(self):
        import json

        try:
            page = int(self.request.get('page'))
            size = int(self.request.get('size'))
            kwidx = str(self.request.get('kwidx'))
            city = str(self.request.get('city'))

            dl = int(self.request.get('dl'))

            if not kwidx == 'all':
                kwidx = int(kwidx)
                if kwidx < 0 or kwidx > (len(Q_TERMS)-1):
                    raise Exception("kwidx")

            if not city == 'all':
                if not city in [o[0] for o in GEO_LIST]:
                    raise Exception("city") 

            if not dl in [0,1]:
                raise Exception("dl")

            if not kwidx == 'all' and not city == 'all':
                raise Exception('index')

        except Exception, e:
            self.response.out.write("<h3>Please supply valid [page] [size] [kwidx] [city] [dl] para</h3>\
                                    <strong>at least one of [kwidx] [city] must be all</strong> \
                                    </br></br>\
                                    [page] start from <i>1</i> <br>\
                                    [size] page size, positive int, suggest <i>10000</i> <br>\
                                    [kwidx] start from 0 to %d in %s or use <i>all</i><br>\
                                    [city] in  %s or use <i>all</i> <br>\
                                    [dl] 0 or 1 whether to download\
                                    " % (len(Q_TERMS)-1,str(Q_TERMS),str([o[0] for o in GEO_LIST])))
            return


        if kwidx == 'all' and city == 'all':
            tws = Tweet.query().fetch(size,offset=(page-1)*size)
        elif kwidx == 'all':
            tws = Tweet.query(Tweet.searchGeo == GEO_DICT[city]).order(Tweet.timestamp).fetch(size,offset=(page-1)*size)
        elif city == 'all':
            tws = Tweet.query(Tweet.searchTerm == Q_TERMS[kwidx]).order(Tweet.timestamp).fetch(size,offset=(page-1)*size)
            

        jd = json.dumps([t.to_dict() for t in tws],default=json_date_handler)
        self.response.headers['Content-Type'] = 'application/json'
        
        if dl == 1:
            self.response.headers['Content-Disposition'] = "attachment;filename=Tweet.size-%d.page-%d.kwidx-%s.city-%s.cnt%d.json" % (size,page,str(kwidx),city,len(tws))
        
        self.response.out.write(jd)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        

        dicts = [o.to_dict() for o in DJI.query().order(DJI.timestamp).fetch()]
        dots = [{'x':d['dji'],'y':str(d['timestamp'])} for d in dicts]
        
        template_values = {
            'dji':dots
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render(template_values))


class TestHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get('q')
        if q is None or q is '':
            q = 'yale'
        geocode = '37.781157,-122.398720,100mi'

        if Tweet.query(Tweet.searchTerm==q).count() > 0:
            since_id = Tweet.query(Tweet.searchTerm==q).order(-Tweet.id).fetch(1)[0].id
        else:
            since_id = 0

        rst = api.search(q=q,geocode=geocode,since_id=since_id,count=100)

        template_values = {
            'tweets':rst
        }
        template = JINJA_ENVIRONMENT.get_template('test.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    # ('/I_am_sure_to_delete_all_ndb',NDBDeleteAllHandler),
    ('/test',TestHandler),
    ('/cron_fetch_tweet',CronFetchTweetHandler),
    ('/cron_fetch_dji',CronFetchDJIHandler),
    ('/cron_dummy',CronDummyHandler),
    ('/ndb_stats',NDBStatsHandler),
    ('/ndb_delete',NDBDeleteHandler),
    
    ('/json_tws_tmp',TweetJsonDumpHandler),
    

    ('/json_tws',TweetJsonDownloadHandler),
    ('/json_dji',DJIJsonHandler)
 
], debug=True)
