import os
from boto.mturk.connection import MTurkConnection
import requests
import json
from db import db

databaseUser = db('heroku_lmx991zw','users')
slackUrl = 'https://hooks.slack.com/services/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'

def printSomething():
	print "something"

def get_all_reviewable_hits(mtc):
    page_size = 50
    hits = mtc.get_reviewable_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    return hits

def pollTurk():
	ACCESS_ID=os.environ['ACCESS_KEY_ID']
	SECRET_KEY=os.environ['SECRET_ACCESS_KEY']
	HOST = 'mechanicalturk.amazonaws.com'

	mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

	hits = get_all_reviewable_hits(mtc)
 
	for hit in hits:
	    assignments = mtc.get_assignments(hit.HITId)
	    for assignment in assignments:
	        print "Answers of the worker %s" % assignment.WorkerId
	        for question_form_answer in assignment.answers[0]:
	            for key in question_form_answer.fields:
	                print "%s" % (key)
	                #find the username based on hitID assignmentID
	                username = databaseUser.getUsernameFromHitID(hit.HITId)
	                diaryEntry=databaseUser.getDiaryEntryFromHitID(hit.HITId)
	                print "username is %s" % (username)
	                print "diaryEntry is %s" % (diaryEntry)
	                #insert assignmentID and response for the user
	                databaseUser.updateResponse(username,assignment.AssignmentId,key)
	                r = requests.post(slackUrl, data=json.dumps({'text':"----------------\n"+username+" wrote \n"+diaryEntry+"\n mTurk response \n" + key+'\n----------------'}))
	        #mtc.approve_assignment(assignment.AssignmentId)
	        print "--------------------"
	    #mtc.disable_hit(hit.HITId)
