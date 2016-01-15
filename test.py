
from db import db

databaseUser = db('heroku_lmx991zw','users')

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