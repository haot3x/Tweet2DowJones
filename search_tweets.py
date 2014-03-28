from TwitterAPI import TwitterAPI,TwitterOAuth


SEARCH_TERM = 'pizza'


o = TwitterOAuth.read_file()

# Using OAuth1...
api = TwitterAPI(
                 o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)

r = api.request('search/tweets', {'q': SEARCH_TERM})

for item in r:
    print(item['text'] if 'text' in item else item)

print('\nQUOTA: %s' % r.get_rest_quota())
