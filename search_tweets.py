from TwitterAPI import TwitterAPI,TwitterOAuth
import sqlite3
conn = sqlite3.connect('test.db')

SEARCH_TERM = 'pizza'
o = TwitterOAuth.read_file()
# Using OAuth1...
api = TwitterAPI(
                 o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)

r = api.request('search/tweets', {'q': SEARCH_TERM})

#https://dev.twitter.com/docs/api/1.1/get/search/tweets
#
# create table test_tweet(created_at TEXT, text TEXT);

#
#
#
#
cnt = 0
for item in r:
    cnt += 1
    print(item['text'] if 'text' in item else item)
    print(item['created_at'])
    text = item['text']
    created_at = item['created_at']
    conn.execute('INSERT INTO test_tweet VALUES (?,?)',(created_at,text))
    
conn.commit()
conn.close()
print('\n DATABASE commited %d items inserted\n' % (cnt,))

print('\nQUOTA: %s' % r.get_rest_quota())
