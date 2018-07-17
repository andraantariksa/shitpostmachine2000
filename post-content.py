from lib.database import *
from lib.line import *
from lib.facebookapi import *

dbcursor.execute("SELECT * FROM post WHERE approval = 'waiting'")
rowPost = dbcursor.fetchone()

"""
LINE POST
"""
dbcursor.execute("SELECT * FROM cookie")
row = dbcursor.fetchone()
cookie = row['cookie']
line = LINE({
	'cookie' : cookie,
	'id' : '11702069'
})
csrf_token = line.initializePost()
imageData = line.uploadImage({
	'csrf_token' : csrf_token,
	'file' : 'post-assets/'+rowPost['content'],
})
postData = {
	'text' : 'Source: '+rowPost['source'],
	'csrf_token' : csrf_token,
}
postData['image[1]'] = {}
postData['image[1]']['id'] = imageData['media']['objectId']
postData['image[1]']['width'] = imageData['media']['width']
postData['image[1]']['height'] = imageData['media']['height']
line_post_id = line.post(postData)


"""
FACEBOOK POST
"""

fb = FacebookAPI({
	'accessToken': 'EAAAAUaZA8jlABAC8mBSprGaBQmFlNDtUFdsf0VBYH28MtlCOYZAgu1E6xFoZAbZBhCaUolXoLGaEfZChKw0SlOgZAHEZC0OTFErrdSCj1AeZAAOX0JrwGlRpO8D2PRMh0O548fwyzwqddOp1gqJkEZCU5mLHLmiCD99yi4r5yWtR4egZDZD'
})
postData = fb.postImageToOwnedFanspage({
	'imageUrl' : 'http://13.250.121.191/shitpostmachine2000/post-assets/'+rowPost['content'],
	'text' : 'Source: '+rowPost['source'],
})
facebook_post_id = postData['post_id']

dbcursor.execute("UPDATE post SET approval = 'posted', facebook_post_url = 'http://www.facebook.com/"+facebook_post_id+"', line_post_url = 'https://admin-official.line.me/"+line.id+"/home/post/"+line_post_id+"/comments' WHERE id = "+str(rowPost['id']))


db.commit()
dbcursor.close()
db.close()