from pymongo import MongoClient
from bson.json_util import dumps
import time
from datetime import datetime, timedelta, date, time
from helper import getNouns

class db:
	def __init__(self,dbName,collectionName,):
		self.client = MongoClient('mongodb://heroku_lmx991zw:tbh7minpt7ihmbcshkull6nh9a@ds059524.mongolab.com:59524/heroku_lmx991zw')
		#self.client = MongoClient()
		self.db=self.client[dbName]
		self.collection=self.db[collectionName]

	def insertOne(self,entry):
		self.collection.insert_one(entry)

	def insertMany(self,entry):
		self.collection.insert_many(entry)

	def findOne(self,query):
		return self.collection.find_one(query)

	def findMany(self,query):
		return self.collection.find(query)

	def listAll(self):
		return self.collection.find()

	def insertInput(self,userId,text,postId):
		for post in self.findMany({}):
			if userId in post:
				temp =userId+'.text'
				nouns = getNouns(text)
				self.collection.update_one({'name': userId}, {'$push': {temp: {"type":"user","text":text, "created_at": datetime.now(),"nouns":nouns, "post_id":postId}}})
				#self.collection.update_one({'name': userId}, {'$push': {temp: {"type":"user","text":text, "created_at": datetime.now()}}})

	def insertReply(self,userId,text,postId,commentFormType,score=0):
		for post in self.findMany({}):
			if userId in post:
				temp =userId+'.text'
				self.collection.update_one({'name': userId}, {'$push': {temp: {"type":"bot","text":text, "afinn_score": score, "created_at": datetime.now(), "post_id":postId,"commentFormType":commentFormType}}})

	def updateCFT(self,userId,cft):
		for post in self.findMany({}):
			if userId in post:
				temp =userId
				self.collection.update_one({'name': userId}, {'$push': {temp: {"cft":cft}}})

	def listAllText(self,userId):
		for post in self.findMany({}):
			if userId in post:
			#	if 'text' in post:
				#print(post)
				return post[userId]['text']
			#	else:
			#		return []

	def getCommentsForWeek(self,userId):
		days = {}
		currentDate = datetime.combine(date.today(), time(0,0))

		for x in range(0,7):
			startDate = (currentDate - timedelta(days=x))
			endDate = (startDate + timedelta(days=1))
			startDateUnix = startDate.strftime('%s')
			endDateUnix = endDate.strftime('%s')

			days[startDateUnix] = []

			temp = userId+'.text'
			# TODO: HOW IS TEXT STORED IN A KEY WITH THE USERNAME? THIS SEEMS DUMB AND NON-STANDARD
			# results = self.collection.find({'name': userId, temp: {'created_at': {'$elemMatch': {'$gte': startDateUnix, '$lt': endDateUnix}}}})
			results = self.collection.find({'name': userId})
			for post in results:
				days[startDateUnix] = post[userId]['text']
				break

		return days

	def insertLastHit(self,userId,text,hitID):
		for post in self.findMany({}):
			if userId in post:
				self.collection.update_one({
											'name': userId
											}, 
											{'$set': {'lastHit':{'text':text,
																'hitID':hitID,
																'response':"",
																'assignmentID':""
																}}})

	def insertSetSession(self,userId,name,value):
		for post in self.findMany({}):
			if userId in post:
				self.collection.update_one({
											'name': userId
											}, 
											{'$set': {name:value}}
											)

	def getSession(self,userId):
		for post in self.findMany({}):
			if userId in post:
				return post['sessionData']
