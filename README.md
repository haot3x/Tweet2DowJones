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



##links
- http://tweet2dowjones.appspot.com/
- http://tweet2dowjones.appspot.com/test?q=ted
- http://tweet2dowjones.appspot.com/ndb_stats
- http://tweet2dowjones.appspot.com/json_dump?q=searchterm
- http://tweet2dowjones.appspot.com/json_dump
- http://tweet2dowjones.appspot.com/ndb_delete?q=searchterm
- tweet2dowjones.appspot.com/I_am_sure_to_delete_all_ndb
- http://tweet2dowjones.appspot.com/json_dump_download?size=10000&page=1

##cron job
- http://tweet2dowjones.appspot.com/cron_fetch_tweet
- http://tweet2dowjones.appspot.com/cron_fetch_dji
	
	
# design
    <script src="/json/json_data.js"></script>

in side `index.html` defines the json data being used
`DATA_XXX` is in the form `{"series":[[],[]],"name":"XYZ"}`

then data series is put inside `jqplot` in the `index.html` javascript part

the directory dev inside /json has a `gen.py` script used to generate dummy classified data from the real input json file, please take a look and change the input/output name

    
	


