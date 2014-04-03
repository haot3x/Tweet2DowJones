import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="63c0lXM51rxZ2cZUr3QcKKR9q"
consumer_secret="Kxu44kTkweAkfAVtYVTe2y2Q8FdtkkKFPaMacyihRs1d9eRuU4"

CONSUMER_KEY = '63c0lXM51rxZ2cZUr3QcKKR9q'
CONSUMER_SECRET = 'Kxu44kTkweAkfAVtYVTe2y2Q8FdtkkKFPaMacyihRs1d9eRuU4'
ACCESS_TOKEN_KEY = '37201527-wnO8ILKImZ4SDzTNF3RNTQ9UMZV4oYeBF0t5lA2yU'
ACCESS_TOKEN_SECRET = 'QHkYL3Vk0E1sj4WPPe2EKb1KbEke0SuW3K0Y6Ag4N4GeS'


# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="37201527-wnO8ILKImZ4SDzTNF3RNTQ9UMZV4oYeBF0t5lA2yU"
access_token_secret="QHkYL3Vk0E1sj4WPPe2EKb1KbEke0SuW3K0Y6Ag4N4GeS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print api.me().name

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's 
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status('Updating using OAuth authentication via Tweepy!')
