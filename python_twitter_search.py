#!/usr/bin/env python
#----------------------------------------------------------------------
# February 6, 2019
#
# Before using, you are required to have a Twitter Developer Account
# in order to get the Consumer and OAuth Tokens.
#
# The accompanying config.py file is used to hold the authentication
# tokens for the user. If the file isn't filled out from default or if
# the file is missing in its entirety, the user can still provide this
# information manually.
#
# This Python takes user input to do a basic Twitter search based on
# key words or phrases provided by the user. The user can provide a 
# list of words or phrases (strings) separating each item with a comma.
# The user is then prompted for any specific user names to search for.
# Twitter API will return either the exact user name or those simiar in
# the event the provided user name was ambiguous. The basic user info
# is provided as well as a list of recent tweets.
#----------------------------------------------------------------------


import twitter
import sys

#----------------------------------------------------------------------
# load our API credentials from config.py
#----------------------------------------------------------------------
import config



#----------------------------------------------------------------------
# Create class to handle Twitter API
#----------------------------------------------------------------------

class Twit:
	def __init__ (self, name):
		self.auth = ""
		self.name = name
		self.consumerKey = ""
		self.consumerSecret = ""
		self.oathToken = ""
		self.oathTokenSecret = ""
	
	def add_keys(self, consumerKey, consumerSecret, oathToken, oathTokenSecret):
		self.consumerKey = consumerKey
		self.consumerSecret = consumerSecret
		self.oathToken = oathToken
		self.oathTokenSecret = oathTokenSecret
		
	def authenticate(self):
		auth = (twitter.oauth.OAuth(self.oathToken,
						self.oathTokenSecret,
						self.consumerKey,
						self.consumerSecret))
		return auth



def main():

	#----------------------------------------------------------------------
	# Create default values in the event there is no config file, get from
	# user
	#----------------------------------------------------------------------
	cfg = True
	basicSearch = []
	userSearch = []

	#----------------------------------------------------------------------
	# create twitter API object from config.py
	#----------------------------------------------------------------------
	try:
		initAccount = Twit(config)
		initAccount.add_keys(config.consumer_key,
						config.consumer_secret,
						config.access_key,
						config.access_secret)
		#----------------------------------------------------------------------
		# make sure the config file has been changed from defaults
		#----------------------------------------------------------------------
		if ((initAccount.consumerKey) == (initAccount.consumerSecret)):
			print("!!!!!!!")
			raise Exception('Config file has not been set!!!!')
		auth = (initAccount.authenticate())
		
	#----------------------------------------------------------------------
	# In case there was an issue retrieving input (ie: if the document is
	# missing or can't read data)
	#----------------------------------------------------------------------
	except:
		print("There are no loaded credentials. Please provide Twitter Developer credentials")
		cfg = False # flag used for config.py file.
	if cfg:
		twitter_api = twitter.Twitter(auth=auth)
	#----------------------------------------------------------------------
	# create twitter API object from user input
	#----------------------------------------------------------------------
	else:
		name = input("What would you like to name this account? ")
		account = Twit(name)
		account.add_keys(input("Consumer Key: "),
			input("Consumer Secret Key: "),
			input("OATH Token: "),
			input("OATH Secret Token: "))
		auth = (account.authenticate())
		twitter_api = twitter.Twitter(auth=auth)
	
	#----------------------------------------------------------------------
	# Gather user input for basic and user search
	#----------------------------------------------------------------------
	
	temp_string = input("\n\nEnter words or phrases for a basic Twitter Search (separate by comma: )\n")
	basicSearch = temp_string.split(",")
	temp_string = input("\n\nEnter any specific Twitter users you would like to search (separate by comma: )\n")
	userSearch = temp_string.split(",")
	
	#----------------------------------------------------------------------
	# perform a basic search of the words or phrases entered by end user
	#----------------------------------------------------------------------
	
	for ITEM in basicSearch:
		try:
			print("\n\n*************************************************")
			print("Searching for " + ITEM)
			print("*************************************************")
			query = twitter_api.search.tweets(q = ITEM)
		#----------------------------------------------------------------------
		# If the connection to Twitter fails, catch exception, throw error,
		# exit program. This often happens with incorrect credentials.
		#----------------------------------------------------------------------
		except Exception  as err:
			print("\nThere was an error!!!!!\n")
			print(err)
			print("\nApplication is now exiting. Please double check authentication input.\n")
			sys.exit(1)
		
		#----------------------------------------------------------------------
		# How long did this query take?
		#----------------------------------------------------------------------
		print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))

		#----------------------------------------------------------------------
		# Loop through each of the results, and print its content.
		#----------------------------------------------------------------------
		for result in query["statuses"]:
			print("(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"]))
			
	#----------------------------------------------------------------------
	# Perform a user search of the Twitter users requested by the end user
	# There is an odd effect of input an ambiguous string and a return of
	# many 'similarly' named users instead of a single user.
	#----------------------------------------------------------------------
	for ITEM in userSearch:
		try:
			print("\n\n*************************************************")
			print("Searching for " + ITEM)
			print("*************************************************")
			query = twitter_api.users.search(q = '"%s"' %ITEM)
		#----------------------------------------------------------------------
		# If the connection to Twitter fails, catch exception, throw error,
		# exit program. This often happens with incorrect credentials.
		#----------------------------------------------------------------------
		except Exception  as err:
			print("\nThere was an error!!!!!\n")
			print(err)
			print("\nApplication is now exiting. Please double check authentication input.\n")
			sys.exit(1)

		#----------------------------------------------------------------------
		# Loop through each of the user results, and print its content.
		#----------------------------------------------------------------------
		for result in query:
			print("(%s) @%s %s" % (result["screen_name"], result["name"], result["location"]))
			#----------------------------------------------------------------------
			# Since Twitter has decided which users best fit the user input, we use
			# the returned user to pull Tweets from their timeline.
			#----------------------------------------------------------------------
			try:
				tweets = twitter_api.statuses.user_timeline(screen_name = result["screen_name"])
				for status in tweets:
					print("(%s) %s" % (status["created_at"], status["text"].encode("ascii", "ignore")))
			#----------------------------------------------------------------------
			# If the retrieval of tweets fail, throw an alert. This has happened
			# in testing with errors stating that I do not have permission to view
			# the users tweets. In this case, throw alert and move on.
			#----------------------------------------------------------------------
			except Exception as err:
				print("There was an error retrieving information for %s \n" % result["screen_name"])
				print(err)
	

main()