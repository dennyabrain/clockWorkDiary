
from db import db

databaseUser = db('heroku_lmx991zw','users')

'''
for post in databaseUser.findMany({}):
    if 'abrainB' in post:
        databaseUser.collection.update_one({
                                    'name': 'abrainB'
                                    }, 
                                            {'$set': {'lastHit.response':"test",
                                                    'lastHit.assignmentID':"assignmentID"
                                                    }
                                            }
                                    )
'''
#find username based on HitID

for post in databaseUser.findMany({}):
	if "lastHit" in post:
		if post['lastHit']['hitID']=='3BPP3MA3TBJUZWFEFB8JXUU8AOTELY':
			print post["name"]