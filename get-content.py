from lib.database import *
from lib.facebookapi import *
from lib.image import *
from lib.reddit import *
import time
import datetime
import json
import os
import html

fanspageList = [
	'Shitposting2006',
	'InternetTouristGuideII',
	'TopDankestMemes',
	'ocfreshstolenmemes1',
	'memesupremeofficial',
]
img = Image()

fb = FacebookAPI({
	'accessToken': 'EAAAAUaZA8jlABAC8mBSprGaBQmFlNDtUFdsf0VBYH28MtlCOYZAgu1E6xFoZAbZBhCaUolXoLGaEfZChKw0SlOgZAHEZC0OTFErrdSCj1AeZAAOX0JrwGlRpO8D2PRMh0O548fwyzwqddOp1gqJkEZCU5mLHLmiCD99yi4r5yWtR4egZDZD'
})
for fanspageIteration in fanspageList:
	fanspageContent = fb.getFanspageContent(fanspageIteration)
	for contentIteration in fanspageContent['data']:
		contentSegment = []
		postData = fb.getImageURL(contentIteration['id'])
		if len(postData['attachments']['data']) == 1 and postData['attachments']['data'][0]['type'] == 'photo':
			img.saveImage('tempfile.tmp', postData['attachments']['data'][0]['media']['src'])
			md5 = img.md5Check('tempfile.tmp')
			extension = img.getImageMIME('tempfile.tmp')
			dbcursor.execute("SELECT * from post WHERE content LIKE '%" + md5 + "%'")
			row_count = dbcursor.rowcount
			if row_count == 0:
				contentSegment.append(md5 + '.' + extension)
				if os.path.isfile('post-assets/tempfile.tmp'):
					os.rename('post-assets/tempfile.tmp', 'post-assets/' + md5 + '.' + extension)
				required_data = ("INSERT INTO post(time, content, source) VALUES (%s, %s, %s)")
				data = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), json.dumps(contentSegment), 'https://www.facebook.com/'+postData['attachments']['data']['id'])
				dbcursor.execute(required_data, data)
				try:
					os.remove('post-assets/tempfile.tmp')
				except OSError:
					pass

reddit = Reddit()
subReddit = reddit.getSubRedditPost('dankmemes', 'hot')
for contentIteration in subReddit['data']['children']:
	contentSegment = []
	if contentIteration['pinned'] == false and contentIteration['stickied'] == false:
		img.saveImage('tempfile.tmp', contentIteration['url'])
		md5 = img.md5Check('tempfile.tmp')
		extension = img.getImageMIME('tempfile.tmp')
		dbcursor.execute("SELECT * from post WHERE content LIKE '%" + md5 + "%'")
		row_count = dbcursor.rowcount
		if row_count == 0:
			contentSegment.append(md5 + '.' + extension)
			if os.path.isfile('post-assets/tempfile.tmp'):
				os.rename('post-assets/tempfile.tmp', 'post-assets/' + md5 + '.' + extension)
			required_data = ("INSERT INTO post(time, content, source) VALUES (%s, %s, %s)")
			data = (
			datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), json.dumps(contentSegment),
			'https://www.reddit.com'+contentIteration['permalink'])
			dbcursor.execute(required_data, data)
			try:
				os.remove('post-assets/tempfile.tmp')
			except OSError:
				pass

db.commit()
dbcursor.close()
db.close()
