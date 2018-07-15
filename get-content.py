from lib.database import *
from lib.facebook import *
from lib.image import *
import time
import datetime
import json
import os

fb = Facebook({
	'email' : 'andra.antariksa@gmail.com',
	'password' : 'andra000'
})
fb.login()
fanspageContent = fb.getFanspageContent([
	'Shitposting2006',
	'InternetTouristGuideII',
	'IhavenomemesImustshitpost',
	'TopDankestMemes',
	'ocfreshstolenmemes1',
	'memesupremeofficial',
])
img = Image()
for t in fanspageContent:
	postState = False
	contentSegment = []
	for y in t['content']:
		"""
		img.saveImage('tempfile.tmp',fb.getImageURL(y).replace('&amp;','&'))
		extension = img.getImageMIME('tempfile.tmp')
		print(extension)
		"""
		img.saveImage('tempfile.tmp',fb.getImageURL(y).replace('&amp;','&'))
		md5 = img.md5Check('tempfile.tmp')
		extension = img.getImageMIME('tempfile.tmp')
		dbcursor.execute("SELECT * from post WHERE content LIKE '%"+md5+"%'")
		row_count = dbcursor.rowcount
		if row_count == 0:
			postState = True
			contentSegment.append(md5+'.'+extension)
			if os.path.isfile('post-assets/tempfile.tmp'):
				os.rename('post-assets/tempfile.tmp', 'post-assets/'+md5+'.'+extension)
	if postState == True:
		required_data = ("INSERT INTO post(time, content, source) VALUES (%s, %s, %s)")
		data = (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), json.dumps(contentSegment), t['source'].replace('&amp;','&').replace('m.facebook','www.facebook'))
		dbcursor.execute(required_data,data)
		try:
			os.remove('post-assets/tempfile.tmp')
		except OSError:
			pass
		#break
	#break
db.commit()
dbcursor.close()
db.close()