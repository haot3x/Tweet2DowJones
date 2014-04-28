Tweet2DowJones
==============

Tweet 2 DowJones

	Author: Haotian
	Last Update: 3 Apr 2014

##setup
	sudo pip install tweepy -t .

##dependency
- https://github.com/tweepy/tweepy
- https://dev.twitter.com/docs/streaming-apis/
- http://pythonhosted.org/tweepy/html/api.html?highlight=result 
- https://github.com/mbostock/d3/wiki/API-Reference
- http://www.jqplot.com/


##links
- http://tweet2dowjones.appspot.com/
- http://tweet2dowjones.appspot.com/ndb_stats

##cron job - currently disabled
- http://tweet2dowjones.appspot.com/cron_fetch_tweet
- http://tweet2dowjones.appspot.com/cron_fetch_dji
	
##json dump
- http://tweet2dowjones.appspot.com/json_dji
- http://tweet2dowjones.appspot.com/json_tws?page=1&size=100&kwidx=7&city=all&dl=0

where for **json_tws**
 
    [page] start from 1 
    [size] page size, positive int, suggest 10000 
    [kwidx] start from 0 to 7 in ['i feel', 'i am feeling', "i'm feeling", 'i dont feel', "i'm", 'Im', 'I am', 'makes me'] or use all
    [city] in ['LA', 'NYC', 'CHI', 'ATL'] or use all 
    [dl] 0 or 1 whether to download

**at least one of `kwi]dx` or `city` must be `all`**


##design
    <script src="/json/json_data.js"></script>

in side `index.html` defines the json data being used
`DATA_XXX` is in the form `{"series":[[],[],...],"name":"XYZ"}` where item [] in the outer list is of format `[x,y]` i.e. `[time,value]` i.e `['%Y-%m-%d %H:%M:%S',value]` e.g `["2014-04-28 04:38:29",166.5]`

we can have by GEO and by KEYWORD, each one is represented as two series - one positive one negative, aligned by time

then data series is put inside `jqplot` in the `index.html` javascript part

the directory dev inside /json has a `gen.py` script used to generate dummy classified data from the real input json file, please take a look and change the input/output name

    
	


